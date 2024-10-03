import pandas as pd
import matplotlib.pyplot as plt


class StudentScoreAnalyzer:
    def __init__(self, file_name):
        self.file_name = file_name
        self.df = pd.read_csv(self.file_name)
        self.score_columns = self.df.columns[2:]
        self.df[self.score_columns] = self.df[self.score_columns].apply(pd.to_numeric, errors='coerce')
        self.df = self.df.dropna(how='all', subset=self.score_columns)

    def find_students_who_failed(self):
        students_who_failed_ = self.df[self.df[self.score_columns].lt(50).any(axis=1)]
        return students_who_failed_['Student'].unique().tolist()

    def calculate_mean_scores(self):
        return self.df[self.score_columns].mean()

    def find_top_students(self):
        student_avg_scores = self.df.groupby('Student')[self.score_columns].mean()
        student_avg_scores['Overall Average'] = student_avg_scores.mean(axis=1)
        max_avg = student_avg_scores['Overall Average'].max()
        top_students = student_avg_scores[student_avg_scores['Overall Average'] == max_avg]
        return top_students

    def find_hardest_subject(self):
        mean_scores = self.calculate_mean_scores()
        hardest_subject = mean_scores.idxmin()
        return hardest_subject

    def save_subject_mean_to_excel(self, output_file_name):
        subject_mean_df = self.df.groupby('Semester')[self.score_columns].mean()
        subject_mean_df.to_excel(output_file_name)
        print(f"\nსაგნების საშუალო ქულები სემესტრების მიხედვით შენახულია ფაილში: {output_file_name}")

    def find_improved_students(self):
        df_sorted = self.df.sort_values(by=['Student', 'Semester'])

        def check_improvement(group):
            scores = group[self.score_columns]
            avg_scores = scores.mean(axis=1)
            diff = avg_scores.diff()
            return (diff.dropna() > 0).all()

        improved_students = df_sorted.groupby('Student').filter(check_improvement)
        return improved_students['Student'].unique()

    def calculate_mean_scores_per_semester(self):
        # თითო საგნის საშუალო ქულების გამოთვლა თითო სემესტრში
        subject_mean_df = self.df.groupby('Semester')[self.score_columns].mean()
        return subject_mean_df

    def plot_mean_scores_per_semester(self):
        subject_mean_df = self.calculate_mean_scores_per_semester()

        # სვეტების დიაგრამის აგება საგნების საშუალო ქულებით
        subject_mean_df.plot(kind='bar', figsize=(10, 6), title='საშუალო ქულები თითო საგნისთვის ყველა სემესტრში')
        plt.xlabel('სემესტრები')
        plt.ylabel('საგნების საშუალო ქულა')
        plt.xticks(rotation=45)
        plt.legend(title='საგნები')
        plt.tight_layout()
        plt.show()

    def plot_overall_mean_scores(self):
        # საშუალო საერთო ქულების გამოთვლა თითო სემესტრში
        overall_mean_scores = self.calculate_mean_scores_per_semester().mean(axis=1)

        # ხაზოვანი გრაფიკის აგება საშუალო საერთო ქულებით სემესტრების მიხედვით
        overall_mean_scores.plot(kind='line', marker='o', figsize=(8, 5), title='საშუალო საერთო ქულა სემესტრების მიხედვით')
        plt.xlabel('სემესტრები')
        plt.ylabel('საშუალო საერთო ქულა')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    analyzer = StudentScoreAnalyzer('student_scores_random_names.csv')

    students_who_failed = analyzer.find_students_who_failed()
    print(f"\nსტუდენტები, რომლებიც ვერ ჩააბარეს საგნები:\n{students_who_failed}")

    mean_scores_ = analyzer.calculate_mean_scores()
    print(f"\nსაშუალო ქულები თითო საგნისთვის:\n{mean_scores_}")

    top_students_ = analyzer.find_top_students()
    print("\nსტუდენტი(ები) ყველაზე მაღალი საშუალო ქულით ყველა სემესტრსა და საგანში:\n",
          top_students_[['Overall Average']])

    hardest_subject_ = analyzer.find_hardest_subject()
    print("\nსაგანი, რომელშიც სტუდენტებს ყველაზე მეტად გაუჭირდათ:", hardest_subject_)
    print("საგნის საშუალო ქულა:", mean_scores_[hardest_subject_])

    analyzer.save_subject_mean_to_excel('average_scores_per_subject.xlsx')

    improved_students_ = analyzer.find_improved_students()
    print(f"\nსტუდენტები, რომლებმაც თანმიმდევრულად გააუმჯობესეს ქულები:\n{improved_students_}")

    analyzer.plot_mean_scores_per_semester()

    analyzer.plot_overall_mean_scores()
