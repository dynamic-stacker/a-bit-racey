import cx_Freeze

executables = [cx_Freeze.Executable("a bit racey.py")]

cx_Freeze.setup(
    name="A bit Racey",
    options={"build_exe":{"packages":["pygame","time","math","sys","random"],
                          "include_files":["images/","msc_snds/",".gitignore","a_bit_racey_db.db","db.py"]}},
    executables = executables

    )
