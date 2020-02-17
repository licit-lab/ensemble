<<<<<<< HEAD
def start_vissim():
    import win32com.client as com
    import os
    Vissim =  "Hello"#com.gencache.EnsureDispatch("Vissim.Vissim-64.10")
    Vissim = com.gencache.EnsureDispatch("Vissim.Vissim-32.10")  # Vissim 10 - 64 bit
    # Vissim = com.gencache.EnsureDispatch("Vissim.Vissim")
    GlosaNetworkPath = 'C:\\Users\\Public\\Documents\\GLOSA\\GlosaTrafficLight'
    # 'L:\\UserData\\Kingsley\\GLOSA\\'
    ## Load a Vissim Network:
    Filename = os.path.join(GlosaNetworkPath, 'GlosaTestNetwork2.inpx')
    flag_read_additionally = False  # you can read network(elements) additionally, in this case set "flag_read_additionally" to true
    Vissim.LoadNet(Filename, flag_read_additionally)
    ## Load a Layout:
    Filename = os.path.join(GlosaNetworkPath, 'GlosaTestNetwork2.layx')
    Vissim.LoadLayout(Filename)
    End_of_simulation = 600  # simulation second [s]
    Simulation_Resolution = 1  # simulation second [s]
    Number_Runs = 4
    Simulation_Period = 300
    Vissim.Simulation.SetAttValue('SimRes', Simulation_Resolution)
    Vissim.Simulation.SetAttValue('NumRuns', Number_Runs)
    Vissim.Simulation.SetAttValue('SimPeriod', Simulation_Period)
    FilePath = 'D:\\ImFlow\\version_3_5_3\\AnalysisResults\\Tilburg - Kingsley\\Vissim Dynniq def\\20200124-131129\\ImFlow\\run#001\\log'

    # substr2='"type":2,"distance":'
    # substr_priority2='granted'
    def extract_values(obj, key):
        """Pull all values of specified key from nested JSON."""
        arr = []

        def extract(obj, arr, key):
            """Recursively search for values of key in JSON tree."""
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        extract(v, arr, key)
                    elif k == key:
                        arr.append(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract(item, arr, key)
            return arr

        results = extract(obj, arr, key)
        return results

    def roundItems(List, n):
        List2 = [round(item, n) for item in List]
        return List2

    def getLastAdvice(AdviceList, TimeStamp):
        m = max(TimeStamp)
        List2 = [i for i, j in enumerate(TimeStamp) if j == m]
        LastAdvice = list(map(AdviceList.__getitem__, List2))
        return LastAdvice

    def ListSignalGroup(substr, InputFilename):
        lines = filter(lambda x: substr in x, open(InputFilename))
        lines = list(lines)
        sg1 = []
        if len(lines) != 0:
            lines4 = [item.split('SG') for item in lines]
            sg = [item[-1][0:3] for item in lines4]
            sg = [''.join(['SG', item.rstrip('"')]) for item in sg]
            [sg1.append(x) for x in sg if x not in sg1]
            # print sg1
            # sg = lines4[-1][0:3]
            # [res2.append(x) for x in lines4 if x not in res2]
        return sg1

    def findsubstr(substr, SG_Number, InputFilename):
        SpeedAdvice1 = []
        DistanceAdvice1 = []
        lines = filter(lambda x: (substr in x) and (SG_Number in x), open(InputFilename))
        lines = list(lines)

        if len(lines) != 0:
            lines2 = [item.split(";") for item in lines]
            lines3 = [item[-1] for item in lines2]  # Make line json readable
            TimeStamp = [extract_values(json.loads(item), 'time') for item in lines3]
            SpeedAdvice = [roundItems(extract_values(json.loads(item), 'speed'), 2) for item in lines3]
            SpeedAdvice = getLastAdvice(SpeedAdvice, TimeStamp)[0]
            # SpeedAdvice = SpeedAdvice [-1]# Get the last(or nth)  speed advice for that signal group
            DistanceAdvice = [extract_values(json.loads(item), 'distance') for item in lines3]
            DistanceAdvice = getLastAdvice(DistanceAdvice, TimeStamp)[0]
        # DistanceAdvice=DistanceAdvice[-1] # Get the last  Distance  advice for that signal group

        else:
            SpeedAdvice = SpeedAdvice1
            DistanceAdvice = DistanceAdvice1

        return [SpeedAdvice, DistanceAdvice]

    # SG_List=ListSignalGroup(substr2, InputFilename2)
    # AdviceInfo=findsubstr(substr2,SG_List[0], InputFilename2)
    # print AdviceInfo
    # RIS_List2=[113,117,119,124,124,125,126,127,128,129,130,131,132,133,134,135,136,140,145,146]
    def getSignalGroupAdvice(RIS_Number, SignalGroupNumber, SpeedAdviceString):
        RIS_FileName = ''.join(['risfi_', str(RIS_Number), '.log'])
        InputFilenamek = os.path.join(FilePath, RIS_FileName)
        SG_List = ListSignalGroup(SpeedAdviceString, InputFilenamek)
        AdviceInfo = []
        if SignalGroupNumber in SG_List:
            AdviceInfo = findsubstr(SpeedAdviceString, SignalGroupNumber, InputFilenamek)
        return AdviceInfo

    # MyAdvice= getSignalGroupAdvice(113,'SG102',substr2)
    # print MyAdvice

    def getPriorityList(RIS_Number, SignalGroupNumber, substr):
        veh_list0 = []
        AdviceInfo1 = []
        RIS_FileName = ''.join(['prioEvents_', str(RIS_Number), '.csv'])
        InputFilenamek = os.path.join(FilePath, RIS_FileName)
        lines = filter(lambda x: (substr in x) and (SignalGroupNumber in x), open(InputFilenamek))
        lines = list(lines)
        VehicleSignalGranted = [item.split(',')[3] for item in lines]
        return VehicleSignalGranted

    # VehicleSignalGranted=getPriorityList(113,'SG102',substr_priority2)
    # print VehicleSignalGranted
    # Vehicle.NextNode= Intersection
    # [[0.0, 5.56], [182.0, 252.0]]

    def writeSpeedAdvice():
       # L1 = [[1, 2], [3, 1]]
        #L2 = np.asarray(L1)
        #print(L2)
        # Get several attributes of all vehicles:
        Veh_attributes = Vissim.Net.Vehicles.GetMultipleAttributes(('VehType', 'No'))
        # VehicleSignalGranted = getPriorityList(Signal_Head_Number, Signal_Group_Number, 'granted')

        if len(Veh_attributes) > 0:
            for SignalHead in Vissim.Net.SignalHeads:
                Signal_Head_Number = SignalHead.AttValue('No')  # int( Signal_Head_Number.split('-')[0])
                Signal_Group_Number = SignalHead.AttValue('Name')
                VehicleSignalGranted = getPriorityList(Signal_Head_Number, Signal_Group_Number, 'granted')
                VehicleSignalGranted = [int(item) for item in VehicleSignalGranted]

                # SignalAdvice = getSignalGroupAdvice(Signal_Head_Number, Signal_Group_Number, '"type":2,"distance":')
                Veh_C2X_attributes = [item for item in Veh_attributes if
                                      item[0] == '102' and item[1] in VehicleSignalGranted]
                for cnt_C2X_veh in range(len(Veh_C2X_attributes)):
                    # VehicleSignalGranted = [VehicleSignalGranted[-1]]
                    SignalAdvice = getSignalGroupAdvice(Signal_Head_Number, Signal_Group_Number, '"type":2,"distance":')
                    Vehicle = Vissim.Net.Vehicles.ItemByKey(Veh_C2X_attributes[cnt_C2X_veh][1])
                    Vehicle.SetAttValue('PriorityStatus', 4)
                    Vehicle.SetAttValue('SpeedAdvice', str(SignalAdvice[0]))
                    Vehicle.SetAttValue('DistanceAdvice', str(SignalAdvice[1]))

    for i in range(0, End_of_simulation, Simulation_Resolution):
        Vissim.Simulation.RunSingleStep()
        writeSpeedAdvice()
        print('Using My Code')
    return  Vissim
X=start_vissim()
#print (X)
	# Vissim 10 - 64 bit version
=======
# import win32com.client as com
import os


def another_function():
    Vissim = "my thing"
    return Vissim
>>>>>>> 73290e5903c97f1d0698f7ec4f307cb025a9e77d
