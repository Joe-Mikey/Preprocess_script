import os
import glob
import csv
import xlrd
import os.path
import sys

sys.path.append("..")

def file_extension(path):
    a = os.path.splitext(path)[1]
    pass
    return a

def GetindexFindage(file, excel_path, mode="test"):
    '''
    file 就是index
    '''
    # 提取病人的序号
    file_temp = file
    file_temp1 = file_temp.split('/Brats18_')
    file_temp2 = file_temp1[1]
    file_temp3 = file_temp.split('.npy')
    file_temp4 = file_temp3[0]
    file_temp5 = file_temp4.split('-sub')

    # if mode == "test":
    #     if(file_temp5[1]  == '0'):
    #         CheckFileName = 'Brats18_' + file_temp2
    #         SurvivalTimes = 0
    #
    #         ## 与csv表格中的信息进行判断
    #         with open(excel_path, 'r') as f:
    #             reader = csv.reader(f)
    #             for row in reader:
    #                 if row[0] != 'BraTs18ID':
    #                     if row[0] == CheckFileName:
    #                         SurvivalTimes = row[2]
    #                         SurvivalTimes = int(SurvivalTimes)
    #                         StandardDay = row[4]
    #                         StandardDay = float(StandardDay)
    #                         LnDay = row[5]
    #                         LnDay = float(LnDay)
    #     else:  #will  continue this loop without this sample
    #         SurvivalTimes = 0
    #         StandardDay = 10000
    #         LnDay = 10000
    # else:  #eg:  mode = train
    #     CheckFileName = 'Brats18_' + file_temp2
    #     SurvivalTimes = 0
    #     ## 与csv表格中的信息进行判断
    #     with open(excel_path, 'r') as f:
    #         reader = csv.reader(f)
    #         for row in reader:
    #             if row[0] != 'BraTs18ID':
    #                 if row[0] == CheckFileName:
    #                     SurvivalTimes = row[2]
    #                     SurvivalTimes = int(SurvivalTimes)
    #                     StandardDay = row[4]
    #                     StandardDay = float(StandardDay)
    #                     LnDay = row[5]
    #                     LnDay = float(LnDay)

    CheckFileName = 'Brats18_' + file_temp2
    SurvivalTimes = 0
    ## 与csv表格中的信息进行判断
    with open(excel_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != 'BraTs18ID':
                if row[0] == CheckFileName:
                    SurvivalTimes = row[2]
                    SurvivalTimes = int(SurvivalTimes)
                    StandardDay = row[4]
                    StandardDay = float(StandardDay)
                    LnDay = row[5]
                    LnDay = float(LnDay)
                    age = row[1]
                    age = float(age)

    return SurvivalTimes, LnDay, age


def generate(train,val,test,num):
    # ## 分3类的标准
    short = 0
    medium = 1
    long = 2

    ## 2分类
    # short = 1
    # long = 0

    ##写train.txt文件
    NUM = str(num)
    txtpath = r'/home/ai/gcy/data/preprocessBraTs18_predictos_v0.43-2021/TenCross_Ln/NO' + NUM + '/'
    if not os.path.exists(txtpath):
        os.makedirs(txtpath)

    "生成train.csv"
    for i in train:  # 生成NO1-NO10 十折
        traindata_path = '/home/ai/gcy/data/preprocessBraTs18_predictos_v0.43-2021/fold/Flair/onlyedema/fold' + i
        f = open(txtpath + 'train.csv', 'a', newline='')
        csv_writer = csv.writer(f)
        if True:
            print('Train datasets start')
            path = traindata_path + '/*/*.npy'
            # imglist = glob.glob(os.path.join(traindata_path, label, '/*/*.png'))  # jpg -> png -> nii.gz #这里加了‘/×/’这里的×是病人的文件夹
            imglist = glob.glob(path)
            # print(imglist)
            # with open(txtpath + 'train.txt', 'a')as f:
            #     for img in imglist:
            #         # print(img + ' ' + str(index))
            #         f.write(img + '@' + str(index))
            #         f.write('\n')

            for img in imglist:
                # print(img + ' ' + str(index))
                # if img.find('T2') != -1: # & img.find('T1C_S') == -1:
                if(file_extension(img)==".npy"):
                    SurvivalTimes, StandardDay, age = GetindexFindage(img, './survival_data.csv', mode="test")
                    if SurvivalTimes == 0:
                        continue

                    ## 3 classes
                    if (int(SurvivalTimes) >= 0) & (int(SurvivalTimes) < 300):
                        time = short
                    elif (int(SurvivalTimes) >= 300) & (int(SurvivalTimes) < 450):
                        time = medium
                    elif (int(SurvivalTimes) >= 450):
                        time = long

                    ## 2 classes
                    # if (int(SurvivalTimes) >= 0) & (int(SurvivalTimes) < 650):
                    #     time = short
                    # elif (int(SurvivalTimes) >= 650):
                    #     time = long

                    csv_writer.writerow([img, str(time), str(SurvivalTimes),str(StandardDay),str(age)])
                    print(img)
        f.close()

    "生成val.csv"
    for j in val:
        valdata_path = '/home/ai/gcy/data/preprocessBraTs18_predictos_v0.43-2021/fold/Flair/onlyedema/fold' + j
        f = open(txtpath + 'val.csv', 'a', newline='')  #属性为add
        csv_writer = csv.writer(f)
        ##注意每次都会接在上次的txt文件后面继续写,而不是覆盖
        # I changed code here to generate the val.txt with label 0 or 1
        # for index, label in enumerate(val_labels):
        if True:
            print('Val datasets start')
            valpath = valdata_path + '/*/*.npy'
            # imglist = glob.glob(os.path.join(valdata_path, label, '/×/*.png'))  # jpg -> png -> nii.gz
            imglist = glob.glob(valpath)
            for img in imglist:
                if (file_extension(img) == ".npy"):
                    # print(img + ' ' + str(index))
                    # if img.find('T2') != -1: # & img.find('T1C_S') == -1:
                    SurvivalTimes, StandardDay, age = GetindexFindage(img, './survival_data.csv', mode="test")
                    if SurvivalTimes == 0:
                        continue
                    ## 3 classes
                    if (int(SurvivalTimes) >= 0) & (int(SurvivalTimes) < 300):
                        time = short
                    elif (int(SurvivalTimes) >= 300) & (int(SurvivalTimes) < 450):
                        time = medium
                    elif (int(SurvivalTimes) >= 450):
                        time = long

                    ## 2 classes
                    # if (int(SurvivalTimes) >= 0) & (int(SurvivalTimes) < 650):
                    #     time = short
                    # elif (int(SurvivalTimes) >= 650):
                    #     time = long

                    csv_writer.writerow([img, str(time), str(SurvivalTimes), str(StandardDay), str(age)])
                    print(img)
        f.close()

    "生成test.csv"
    for k in test:
        testdata_path = '/home/ai/gcy/data/preprocessBraTs18_predictos_v0.43-2021/fold/Flair/onlyedema/fold' + k
        f = open(txtpath + 'test.csv', 'a', newline='')  # 属性为add
        csv_writer = csv.writer(f)
        ##注意每次都会接在上次的txt文件后面继续写,而不是覆盖
        # I changed code here to generate the val.txt with label 0 or 1
        # for index, label in enumerate(test_labels):
        if True:
            print('Test datasets start')
            testpath = testdata_path + '/*/*.npy'
            # imglist = glob.glob(os.path.join(testdata_path, label, '/×/*.png'))  # jpg -> png -> nii.gz
            imglist = glob.glob(testpath)
            for img in imglist:
                if (file_extension(img) == ".npy"):
                    # print(img + ' ' + str(index))
                    # if img.find('T2') != -1: # & img.find('T1C_S') == -1:
                    SurvivalTimes, StandardDay, age = GetindexFindage(img, './survival_data.csv', mode="test")
                    if SurvivalTimes == 0:
                        continue

                    ## 3 classes
                    if (int(SurvivalTimes) >= 0) & (int(SurvivalTimes) < 300):
                        time = short
                    elif (int(SurvivalTimes) >= 300) & (int(SurvivalTimes) < 450):
                        time = medium
                    elif (int(SurvivalTimes) >= 450):
                        time = long

                    ## 2 classes
                    # if (int(SurvivalTimes) >= 0) & (int(SurvivalTimes) < 650):
                    #     time = short
                    # elif (int(SurvivalTimes) >= 650):
                    #     time = long

                    csv_writer.writerow([img, str(time), str(SurvivalTimes), str(StandardDay), str(age)])
                    print(img)
        f.close()


if __name__ == '__main__':
    # 1
    NO1_train = ['1','2','3','4','5','6','7','8','remain']
    NO1_val = ['9']
    NO1_test = ['10']
    generate(NO1_train,NO1_val,NO1_test,1)
    # 2
    NO1_train = ['9', '2', '3', '4', '5', '6', '7', '8', 'remain']
    NO1_val = ['10']
    NO1_test = ['1']
    generate(NO1_train, NO1_val, NO1_test, 2)
    # 3
    NO1_train = ['9', '10', '3', '4', '5', '6', '7', '8', 'remain']
    NO1_val = ['1']
    NO1_test = ['2']
    generate(NO1_train, NO1_val, NO1_test, 3)
    # 4
    NO1_train = ['1', '9', '10', '4', '5', '6', '7', '8', 'remain']
    NO1_val = ['2']
    NO1_test = ['3']
    generate(NO1_train, NO1_val, NO1_test, 4)
    # 5
    NO1_train = ['1', '2', '9', '10', '5', '6', '7', '8', 'remain']
    NO1_val = ['3']
    NO1_test = ['4']
    generate(NO1_train, NO1_val, NO1_test, 5)
    # 6
    NO1_train = ['1', '2', '3', '9', '10', '6', '7', '8', 'remain']
    NO1_val = ['4']
    NO1_test = ['5']
    generate(NO1_train, NO1_val, NO1_test, 6)
    # 7
    NO1_train = ['1', '2', '3', '4', '9', '10', '7', '8', 'remain']
    NO1_val = ['5']
    NO1_test = ['6']
    generate(NO1_train, NO1_val, NO1_test, 7)
    # 8
    NO1_train = ['1', '2', '3', '4', '5', '9', '10', '8', 'remain']
    NO1_val = ['6']
    NO1_test = ['7']
    generate(NO1_train, NO1_val, NO1_test, 8)
    # 9
    NO1_train = ['1', '2', '3', '4', '5', '6', '9', '10', 'remain']
    NO1_val = ['7']
    NO1_test = ['8']
    generate(NO1_train, NO1_val, NO1_test, 9)
    # 10
    NO1_train = ['1', '2', '3', '4', '5', '6', '7', '10', 'remain']
    NO1_val = ['8']
    NO1_test = ['9']
    generate(NO1_train, NO1_val, NO1_test, 10)