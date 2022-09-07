import stages.clean_data as clean
import stages.show_street as draw
import stages.load_ss_lv as load
import utilz.functions as f


def main():
    download_new_data = f.download_new_data()
    if download_new_data:

        # first stage
        use_proxy = f.needs_proxy()
        load.use_proxy = use_proxy
        mode = load.main()

        # second stage
        clean.mode = mode
        clean.main()

        # third stage
        draw.mode = mode
        draw.main()
    else:
        draw.main()


if __name__ == '__main__':
    main()
