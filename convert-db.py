import csv
import sys


def record_to_filename(record):
    return f"data/{str(record).zfill(4)}.yml"


def split_string(s, split_sequence):
    if s.strip() == "":
        return ["~"]
    for character in split_sequence:
        if character in s:
            return [w.strip() for w in s.split(character)]
    return [s.strip()]


def normalize_usage_label(s):
    s = s.strip()
    if s == "":
        return "~"
    if s == "NA":
        return "~"
    return s


def print_as_yaml_list(string_spreadsheet, split_sequence):
    s = ""
    for line in split_string(string_spreadsheet, split_sequence):
        if ":" in line or "[" in line or "]" in line:
            s += f"  - '{line}'\n"
        else:
            if line.strip() != "":
                s += f"  - {line}\n"
    return s


def write_record(row, record):
    tags = "Actionality,Actuality,Additive,Addressee,Apprehension,Assessment,Attitude,Calculation,Caritive,Causation,Cause,Comitative,Comparison,Condition,Concession,Consequence,Degree of accuracy,Degree of intensity,Discourse structure,Epistemic modality (Degree of certainty),Exceptive,Exclusive,Inclusive,Instrument,Manner,Measure,Mirative,Non-existence,Non-Standard Subject,Options,Phase of action,Pluractionality,Polarity value,Possession,Prohibition,Purpose,Quantification,Reaction to the previous discourse,Request,Result,Root modality,Routine,Salient property,Source of information,Source of opinion,Spatial expression,Subset,Taxis,Temporal expression,Temporary characteristics,Timeline,Threat,Volition".split(
        ","
    )

    split_sequence = ["+", ",", ";", "/"]

    with open(record_to_filename(record), "w") as f:
        f.write("---\n")
        f.write(f"record: {record}\n")
        f.write(f"name: '{row['Name'].strip()}'\n")
        f.write(f"UD_name: '{row['Name UD'].strip()}'\n")
        f.write(f"illustration: '{row['Illustration'].strip()}'\n")
        f.write(f"cefr_level: {row['CEFR level'].strip()}\n")
        f.write("definitions:\n")
        for language in ["Russian", "English", "Norwegian"]:
            entry = row[f"Definition in {language}"].strip()
            if entry != "":
                f.write(f"  - {language.lower()}: |\n")
                f.write(f"       {entry}\n")
        f.write("examples:\n")
        for column in ["Example 1", "Example 2", "Example 3", "Example 4", "Example 5"]:
            entry = row[column].strip()
            if entry != "":
                f.write("  - |\n")
                f.write(f"       {entry}\n")
        f.write("morphology:\n")
        f.write(print_as_yaml_list(row["Morphology"], split_sequence))
        f.write("syntactic_type_of_construction:\n")
        f.write(print_as_yaml_list(row["Synt. type of construction"], split_sequence))
        f.write("syntactic_function_of_anchor:\n")
        f.write(print_as_yaml_list(row["Synt. func. of anchor"], split_sequence))
        f.write("syntactic_structure_of_anchor:\n")
        f.write(print_as_yaml_list(row["Synt. structure of anchor"], split_sequence))
        f.write("part_of_speech_of_anchor:\n")
        f.write(print_as_yaml_list(row["Part of speech of anchor"], split_sequence))
        f.write("semantic_roles:\n")
        f.write(print_as_yaml_list(row["Semantic role"], split_sequence))
        f.write("intonation:\n")
        f.write(
            print_as_yaml_list(
                row["Communicative type"],
                split_sequence,
            )
        )
        f.write(f"usage_label: {normalize_usage_label(row['Usage label'])}\n")

        f.write("dependency_structure:\n")
        f.write(print_as_yaml_list(row["Dependency Structure"], split_sequence))
        f.write("dependency_structure_of_illustration:\n")
        f.write(
            print_as_yaml_list(
                row["Dependency Structure of Illustration"].replace("\\n", " "),
                ["+"],
            )
        )

        entry = row["Comment"].strip()
        if entry != "":
            f.write("comment: |\n")
            f.write(f"    '{entry}'\n")

        f.write("common_fillers:\n")
        f.write(
            print_as_yaml_list(
                row["Common fillers"],
                split_sequence,
            )
        )

        f.write("references:\n")
        f.write("  - |\n")
        f.write("    " + row["References"].strip() + "\n")
        f.write("semantic_types:\n")
        for tag in tags:
            if row[tag] != "":
                f.write(f"  - type: {tag}\n")
                if row[tag] != "Unspecified":
                    f.write(f"    subtypes:\n")
                    for chunk in row[tag].split(", "):
                        if ":" in chunk:
                            first, second = chunk.split(":")
                            f.write(f"      - type: {first.strip()}\n")
                            f.write(f"        subtypes:\n")
                            f.write(f"          - type: {second.strip()}\n")
                        else:
                            f.write(f"      - type: {chunk.strip()}\n")
        f.write("family:\n")
        f.write("  - |\n")
        f.write('    "' + row["Family"] + '"\n')


if __name__ == "__main__":
    with open(sys.argv[-1], "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = int(row["ID Number"])
            write_record(row, record)
