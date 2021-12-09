
import astronomy as a
def make_dir(dir_name):
    try:
        if os.path.isdir(str(Path().absolute()) + f"\\{dir_name}\\"):
            pass
        else:
            os.makedirs(str(Path().absolute()) + f"\\{dir_name}\\")
    except:
        print(f"Raised Exception trying to create {dir_name} directory.")
    return
  
def main():
    global start_week, end_week, start_eng_range, end_eng_range
    start_week, end_week, start_eng_range, end_eng_range = a.do_some_prompts()
    a.download_some_files(start_week, end_week)
    make_dir("Occurrence-singles")
    make_dir("Occurrence-avgs")
    make_dir("Energy-singles")
    make_dir("Energy-avgs")
    a.procedural_gen_full(start_week, end_week, start_eng_range, end_eng_range)
main()

