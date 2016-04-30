from difflib import SequenceMatcher
import os
import sys


def find_similar(blacklist=None, threshold=0.6, path=os.getcwd(),
                 pair_programming=False, file_types=None, min_file_length=-1):
    if blacklist is None:
        blacklist = []

    if file_types is None:
        file_types = [".py", ".java", ".js"]

    homework_submissions = []

    for root, directories, files in os.walk(path):
        for filename in files:
            for file_type in file_types:
                blacklisted = False
                for item in blacklist:
                    if filename.lower() == item.lower():
                        blacklisted = True

                if filename.endswith(file_type) and not blacklisted:
                    curr_path = os.path.join(root, filename)

                    hw_file = open(curr_path)
                    contents = hw_file.read()
                    hw_file.close()

                    if min_file_length == -1 or len(contents) >= min_file_length:
                        homework_submissions.append((curr_path, contents))
                    break

    number_of_submissions = len(homework_submissions)
    print("Evaluating {} file{}.\n".format(number_of_submissions, "s" if number_of_submissions != 1 else ""))

    comparisons_completed = 0
    total_similarity = 0.0
    total_ratios = 0
    discovered_pairs = []

    for file_1 in homework_submissions:
        sequence_matcher = SequenceMatcher(None, file_1[1])

        for file_2 in homework_submissions:
            comparisons_completed += 1

            name_2 = file_2[0][file_2[0].find(path + "/") + len(path + "/"):file_2[0].find("(")]

            if pair_programming and name_2.split(", ")[0] in file_1[1] and name_2.split(", ")[1] in file_1[1]:
                continue

            if file_1 == file_2:
                continue

            sys.stdout.write("Progress: {:.2f}%\r".format((comparisons_completed / number_of_submissions ** 2) * 100))
            sys.stdout.flush()

            sequence_matcher.set_seq2(file_2[1])
            total_ratios += 1

            ratio = sequence_matcher.real_quick_ratio()
            if ratio < threshold:
                total_similarity += ratio
                continue

            ratio = sequence_matcher.quick_ratio()
            if ratio < threshold:
                total_similarity += ratio
                continue

            ratio = sequence_matcher.ratio()
            if ratio > threshold and (file_2, file_1) not in discovered_pairs:
                discovered_pairs.append((file_1, file_2))
                print("File 1: {}\nFile 2: {}\nSimilarity: {:.2f}%\n\n".format(file_1[0], file_2[0], ratio * 100))

            total_similarity += ratio

    print("Progress: 100.00%")
    print("Average Similarity: < {:.2f}%".format(((total_similarity / total_ratios) * 100)  if total_ratios > 0 else 0))
