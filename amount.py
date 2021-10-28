# -*- coding:utf-8 -*-
import subprocess
def getDiskList():
  new_arr = []
  child = subprocess.Popen(['fdisk','-l'],stdout=subprocess.PIPE)
  child.wait()
  a = child.stdout.readlines()
  for i in range(len(a)):
    disk = a[i].decode('utf8')
    if disk.startswith("/dev/"):
      if "T" in disk:
        new_arr.append(disk.split(" ")[0])
  return new_arr

def getDiskUUID():
  new_arr = []
  child = subprocess.Popen(['blkid'],stdout=subprocess.PIPE)
  child.wait()
  a = child.stdout.readlines()
  for i in a:
    if len(i.decode('utf8')) > 0:
      dlist = []
      disk_detail = i.decode('utf8')
      p = disk_detail.split(":")
      dlist.append(p[0])
      d = p[1].split(" ")
      for x in d:
        e = x.split("=")
        for y in range(len(e)):
          if e[y].startswith('UUID'):
            dlist.append(eval(e[y+1]))
          if e[y].startswith('TYPE'):
            dlist.append(eval(e[y+1]))
      new_arr.append(dlist)

  return new_arr
    
  return new_arr
def getNewArr(disk_list,disk_uuid):
    new_data = []
    for i in disk_uuid:
        for x in disk_list:
          if x in i:
            new_data.append(i)
    return new_data

if __name__ == '__main__':
  disk_list = getDiskList()
  disk_uuid = getDiskUUID()
  dlist = getNewArr(disk_list,disk_uuid)
  if len(dlist) > 0:
    fstab = ""
    for i in range(len(dlist)):
      number = str(i+1)
      x = "UUID="+dlist[i][1]+"\t/plots/plots"+number.zfill(2)+"\t"+dlist[i][2]+"\tnosuid,nodev,nofail,x-systemd.automount,x-gvfs-show,x-systemd.device-timeout=30\t0\t0\n"
      fstab += x
    with open("/etc/fstab", "w+") as fh:
      fh.write(fstab)