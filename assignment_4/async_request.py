import aiohttp
import asyncio
import json
import time
import aiofiles


class PostFetcher:
    def __init__(self, post_count: int = 77):
        if post_count <= 0:
            raise ValueError("post_count must be greater than 0")
        if post_count > 100:
            print("WARNING: post_count cannot be greater than 100")

        self.API = "https://jsonplaceholder.typicode.com/posts/{post_id}"
        self.response_times = []
        self.output_file = "data.json"
        self.response_file = "response_times.json"
        self.post_count = post_count if post_count <= 100 else 100
        self.file_lock = asyncio.Lock()

    async def fetch_post(self, post_id):
        start_time = time.time()
        print(f'Sending request to {post_id}')

        async with aiohttp.request("GET", self.API.format(post_id=post_id)) as response:
            duration = time.time() - start_time
            if response.status != 200:
                print(f"Error fetching post {post_id}")
                return None

            post_data = await response.json()
            self.response_times.append((post_id, duration))

            async with self.file_lock:
                await self.append_to_json_file(post_data)

            print(f"Got post data: {post_id}")

    async def append_to_json_file(self, data):
        async with aiofiles.open(self.output_file, "a", encoding="utf-8") as file:
            await file.write(json.dumps(data, ensure_ascii=False, indent=4) + ",\n")

    @staticmethod
    async def overwrite_last_char(file_path, new_char):
        async with aiofiles.open(file_path, 'r+b') as file:
            await file.seek(0, 2)
            file_size = await file.tell()

            if file_size > 0:
                await file.seek(file_size - 3)
                await file.write(new_char.encode('utf-8'))

                await file.truncate()

    async def main(self):
        start_time = time.time()

        async with aiofiles.open(self.output_file, "w", encoding="utf-8") as file:
            await file.write("[\n")

        tasks = [
            self.fetch_post(post_id)
            for post_id in range(1, self.post_count + 1)
        ]
        await asyncio.gather(*tasks)

        await self.overwrite_last_char(self.output_file, ']')

        elapsed_time = time.time() - start_time

        fastest_response = min(self.response_times, key=lambda x: x[1])
        slowest_response = max(self.response_times, key=lambda x: x[1])

        print(f"Fetching all posts took {elapsed_time:.2f} seconds.")
        print(f"Fastest response: Post ID {fastest_response[0]} took {fastest_response[1]:.2f} seconds.")
        print(f"Slowest response: Post ID {slowest_response[0]} took {slowest_response[1]:.2f} seconds.")

        async with aiofiles.open(self.response_file, "w", encoding="utf-8") as file:
            await file.write(json.dumps({
                "total_time": elapsed_time,
                "fastest_response": fastest_response,
                "slowest_response": slowest_response,
                "response_times": dict(self.response_times)
            }, indent=4))


if __name__ == "__main__":
    fetcher = PostFetcher()
    asyncio.run(fetcher.main())
