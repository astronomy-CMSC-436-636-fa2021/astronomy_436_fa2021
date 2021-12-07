import astronomy as a
def main():
    global start_week, end_week, start_eng_range, end_eng_range
    start_week, end_week, start_eng_range, end_eng_range = a.do_some_prompts()
    a.download_some_files(start_week, end_week)
    try:
        if a.os.path.isdir(str(a.Path().absolute()) + f"\\outputs\\"):
            pass
        else:
            a.os.makedirs(str(a.Path().absolute()) + f"\\outputs\\")
    except:
        print("Raised Exception")
    a.procedural_gen_full(start_week, end_week, start_eng_range, end_eng_range)


main()