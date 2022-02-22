

## Preparation
1. check crontab is installed or not
```
crontab -l
```
2. Install crontab if not
```
sudo apt-get install cron
```

---
## Edit crontab
3. Open up crontab editor
**Note:**Reboot cannot be done usually due to user access control in Ubuntu, we need to put up under SuperUser:
```
sudo crontab -e
```

4. To be added in crontab
```
55 23 * * * bash /home/pi/Raspberrypi-tensorflow-opencv_docker/restart_phase1_in_cron.sh
59 23 * * * /sbin/shutdown -r now
```

5. check whether the entries have been successfully saved
```
sudo crontab -l
```

#### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
