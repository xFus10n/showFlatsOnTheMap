import stages.clean_data as clean
import stages.show_street as draw
import stages.load_ss_lv as load

if __name__ == '__main__':
    load.main()
    clean.main()