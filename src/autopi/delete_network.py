
#!/usr/bin/env python3
"""Delete a network from user input."""


import util.network_info as ni
import util.user_interface as ui
import util.wpa_interface as wpa


def _is_all_or_none(user_input: str) -> bool:
    return user_input.lower() in ("all" or "none")


def _process_output(ssid: str, deleted: bool):
    if deleted:
        print(ssid + " deleted!")
    else:
        print("Failed deleting: " + ssid)


def main():
    ssid = ui.get_input(
        "What is the SSID of the network to be deleted? (case sensitive)",
            validator=wpa.is_valid_ssid,
            error_message=wpa.SSIDLengthError.constraint_msg,
    )
    if ni.check_duplicate_ssid(ssid, wpa.get_default_wpa_config_file()):
        print("Mutiple networks with SSID: " + ssid)
        deletion_choice = ui.get_input("Delete none or all of networks with SSID: " + ssid + "? (all/none)",
        validator=_is_all_or_none)
        if deletion_choice.lower() == "all":
            while ni.check_duplicate_ssid(ssid, wpa.get_default_wpa_config_file()):
                ni.delete_ssid(ssid)
            _process_output(ssid, ni.delete_ssid(ssid))
        else:
            print("No networks deleted!")
    else:
        _process_output(ssid, ni.delete_ssid(ssid))


if __name__ == "__main__":
    main()
