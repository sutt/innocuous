# convert_to_md.py

def convert_to_markdown(input_file="md_input.txt", output_file="md_output.md"):
    with open(input_file, "r", encoding="utf-8") as fin, \
         open(output_file, "w", encoding="utf-8") as fout:
        
        for line in fin:
            # Strip the newline, but preserve empty lines
            stripped = line.rstrip("\n")
            if stripped.strip():  # non-empty line
                fout.write(f"> {stripped}  \n")
            else:  # empty line, just preserve with blockquote
                fout.write(">  \n")

if __name__ == "__main__":
    convert_to_markdown()
