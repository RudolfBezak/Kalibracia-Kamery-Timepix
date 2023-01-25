def merge_files(input_files, output_file):
    with open(output_file, 'w') as f_out:
        lines_per_file = []
        for input_file in input_files:
            with open(input_file, 'r') as f_in:
                lines_per_file.append(f_in.readlines())
        lines_count = len(lines_per_file[0])
        for i in range(lines_count):
            for j in range(len(input_files)):
                f_out.write(lines_per_file[j][i].strip())
                if j != len(input_files) - 1:
                    f_out.write(" ")
            f_out.write("\n")

merge_files(["gerGauss.rudolf", "amGauss.rudolf", "indGauss.rudolf"], "allGauss.rudolf")