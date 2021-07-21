# Memo

`memo` is a small python+shell project aimed at _passive and delicate_ expansion
of the user's vocabulary. It harnesses `notify-send` to show \<phrase-translation\>
pairs on the screen, a `systemd` unit - to start the program on boot, and `anacron` - to regularly
auto-update the vocabulary from a public collection on translate.yandex.ru.

[Яндекс Переводчик](translate.yandex.ru) allows one to collect favorite translations,
amend them, and, most important, make them public, thus, available for automated download.

## Installation

1. Clone the repository  
```git clone https://github.com/lukoshkin/memo.git```
1. Cd to the project folder and run the installation script  
```./install.sh <path2vocab/collection_id>```,  
where as the only argument one specifies the **path to their vocabulary**  
or **the public collection id** on translate.yandex.ru

---

For full functioning (namely, to stop showing word pairs when the user is idle),  
it needs `xprintidle` installed. On Ubuntu, one can install it with

```
sudo apt update && sudo apt install xprintidle
```

## Removal

```
sudo systemctl disable memo.service
sudo sed -i '/update-dict.memo/d' /etc/anacrontab
```

## Troubleshooting

* For some laptops, it is not enough to export just `DISPLAY` variable in the
  systemd unit file, and `DBUS_SESSION_BUS_ADDRESS` is also required. In this case,
  one pastes their value of the latter variable <br> (check it with `echo
  $DBUS_SESSION_BUS_ADDRESS`) in the generated after execution of `install.sh`
  script `memo.service` file, on the same line as the former variable, separating
  them with a space.

  For example,
  ```
  Environment="DISPLAY=:0" "DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus"
  ```

* Due to an unknown bug in `notify-send`, the next notification after
  the user becomes inactive hangs. That does not prevent the program from operating.
  That is, after they click or press a key, it will show all the notifications
  it was going to but could not. A remedy option suitable only to a few laptops
  would be making the opposite to the point above. In other words,
  _if the aforementioned problem is not a problem, then it is the remedy._

