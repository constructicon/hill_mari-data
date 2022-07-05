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
        # f.write(f"UD_name: '{row['Name UD'].strip()}'\n")
        f.write(f"formula_gloss: '{row['Gloss for the formula'].strip()}'\n")

        f.write(f"illustration: '{row['Illustration'].strip()}'\n")
        f.write(f"illustration_gloss_russian: '{row['Gloss for the illustration (Russian)'].strip()}'\n")
        f.write(f"illustration_gloss_english: '{row['Gloss for the illustration (English)'].strip()}'\n")
        f.write(f"illustration_translation_russian: '{row['Translation for the illustration (Russian)'].strip()}'\n")
        f.write(f"illustration_translation_english: '{row['Translation for the illustration (English)'].strip()}'\n")

        f.write("definitions:\n")
        for language in ["Russian", "English"]:
            entry = row[f"Definition in {language}"].strip()
            if entry != "":
                f.write(f"  - {language.lower()}: |\n")
                f.write(f"       {entry}\n")
        f.write("examples:\n")
        for column in ["Example 1: sentence", "Example 2: sentence", "Example 3: sentence"]:
            entry = row[column].strip()
            if entry != "":
                f.write("  - |\n")
                f.write(f"       {entry}\n")
        f.write("examples_glosses_russian:\n")
        for column in ["Example 1: gloss (Russian)", "Example 2: gloss (Russian)", "Example 3: gloss (Russian)"]:
            entry = row[column].strip()
            if entry != "":
                f.write("  - |\n")
                f.write(f"       {entry}\n")

        f.write("examples_glosses_english:\n")
        for column in ["Example 1: gloss (English)", "Example 2: gloss (English)", "Example 3: gloss (English)"]:
            entry = row[column].strip()
            if entry != "":
                f.write("  - |\n")
                f.write(f"       {entry}\n")

        f.write("examples_translation_russian:\n")
        for column in ["Example 1: translation (Russian)", "Example 2: translation (Russian)", "Example 3: translation (Russian)"]:
            entry = row[column].strip()
            if entry != "":
                f.write("  - |\n")
                f.write(f"       {entry}\n")

        f.write("examples_translation_english:\n")
        for column in ["Example 1: translation (English)", "Example 2: translation (English)", "Example 3: translation (English)"]:
            entry = row[column].strip()
            if entry != "":
                f.write("  - |\n")
                f.write(f"       {entry}\n")
        f.write("examples_sources:\n")
        for column in ["Example 1: source", "Example 2: source", "Example 3: source"]:
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

        entry = row["Comment"].strip()
        if entry != "":
            f.write("comment: |\n")
            f.write(f"    '{entry}'\n")

        f.write("references:\n")
        f.write("  - |\n")
        try:
            f.write("    " + row["References"] + "\n")
        # to catch keyerror when encoding symbol appears after getting the csv from xlsx:
        except KeyError:
            f.write("    " + row["\ufeffReferences"] + "\n")
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
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            try:
                record = int(row["ID Number"])
            except ValueError:
                pass
            write_record(row, record)
