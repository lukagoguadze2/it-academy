import requests
import json
import time
import threading


class PostFetcher:
    def __init__(self, post_count: int = 77):
        if post_count <= 0:
            raise ValueError("post_count must be greater than 0")
        if post_count > 100:
            print("WARNING: post_count cannot be greater than 100")

        self.file_lock = threading.Lock()
        self.print_lock = threading.Lock()
        self.response_times = []
        self.output_file = "data.json"
        self.response_file = "response_times.json"
        self.post_count = post_count if post_count <= 100 else 100

    def fetch_post(self, post_id):
        url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

        # Start time of request
        start_time = time.time()

        with self.print_lock:
            print('Sending request to', post_id)

        response = requests.get(url)

        end_time = time.time()
        duration = end_time - start_time

        if response.status_code != 200:
            print("Error fetching post", post_id)
            return None

        post_data = response.json()

        with self.file_lock:
            self.response_times.append((post_id, duration))

            print("Got post data:", post_id)
            with open(self.output_file, "r+", encoding="utf-8") as file:
                try:
                    current_data = json.load(file)
                except json.JSONDecodeError:
                    current_data = []

                current_data.append(post_data)

                file.seek(0)
                json.dump(current_data, file, ensure_ascii=False, indent=4)
                file.truncate()

    def main(self):
        start_time = time.time()

        with open(self.output_file, "w", encoding="utf-8") as file:
            json.dump([], file)

        threads = []

        for post_id in range(1, self.post_count+1):
            thread = threading.Thread(target=self.fetch_post, args=(post_id,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        end_time = time.time()
        elapsed_time = end_time - start_time

        fastest_response = min(self.response_times, key=lambda x: x[1])
        slowest_response = max(self.response_times, key=lambda x: x[1])

        print(f"Fetching all posts took {elapsed_time:.2f} seconds.")
        print(f"Fastest response: Post ID {fastest_response[0]} took {fastest_response[1]:.2f} seconds.")
        print(f"Slowest response: Post ID {slowest_response[0]} took {slowest_response[1]:.2f} seconds.")

        with open(self.response_file, "w", encoding="utf-8") as file:
            json.dump({
                "total_time": elapsed_time,
                "fastest_response": fastest_response,
                "slowest_response": slowest_response,
                "response_times": dict(self.response_times)  # Convert list to dict for JSON serialization
            }, file, ensure_ascii=False, indent=4)

        # sorting response output_file
        with open(self.output_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        with open(self.output_file, "w", encoding="utf-8") as file:
            json.dump(sorted(data, key=lambda item: item['id']), file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    fetcher = PostFetcher()
    fetcher.main()
