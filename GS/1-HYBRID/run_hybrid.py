import glob
import os
import subprocess

passMsg = "\33[92m PASS \33[0m"
failMsg = "\33[91m FAIL \33[0m"

testCases = sorted([f.path for f in os.scandir("./") if f.is_dir()])



for i in testCases:
    """
    check for two output files
    """
    if (len(glob.glob(i+"/*/output.dat")) != 2):
        if os.path.isfile(i+"/PSI4/output.dat")==False:
            print("Running {}".format(i+"/PSI4/"))
            p=subprocess.Popen(['psi4'],cwd=i+"/PSI4/")
            p.wait()
        if os.path.isfile(i+"/PSIXAS/output.dat")==False:
            print("Running {}".format(i+"/PSIXAS/"))
            p=subprocess.Popen(['psi4'],cwd=i+"/PSIXAS/")
            p.wait()


    psi4 = [float(x.split("=")[1]) for x in  open(i+"/PSI4/output.dat").readlines() if "Total Energy = " in x][0]
    psixas = [float(x.split()[4]) for x in open(i+"/PSIXAS/output.dat").readlines() if "FINAL GS SCF ENERGY:" in x][0]
    err = abs(psi4-psixas)
    if (err<1E-6):
        msg = passMsg
    else:
        msg = failMsg
    print("{:25s}: {:16.8f}  {:16.8f}  {:5.02e} {:4s}".format(i,psi4,psixas,err,msg))





