import stages.clean_data as clean
import stages.show_street as draw
import stages.load_ss_lv as load
import utilz.functions as f
import utilz.sources as src


def main():
    download_new_data = f.download_new_data()
    if download_new_data:

        # first stage
        use_proxy = f.needs_proxy()
        load.use_proxy = use_proxy
        mode = load.main()

        # second stage
        clean.main(mode=mode)

        # third stage
        draw.main(mode=mode)
    else:
        option_key, options = f.mode_select(src.linkz, 'Choose flats or houses : ')
        mode = options.get(option_key)
        draw.main(mode)


if __name__ == '__main__':
    main()
