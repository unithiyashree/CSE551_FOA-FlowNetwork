def fileCreator(temp_file_path):
    file_object = "sampleData.txt"
    temp_obj = open(temp_file_path,'w')
    line = ""
    with open(file_object) as fp:
        content = fp.readlines()
    print(len(content))
    for line in content:
        splitted_string = line.split(",")
        splitted_time = splitted_string[2].split(":")
        hour = int(splitted_time[0])
        splitted_time[1] = "00"
        if(splitted_string[0] == "PHX" or splitted_string[0] == "DEN"):
            hour = hour - 1
            if(hour < 0):
                hour = hour + 1
            splitted_time[0] = hour
        if(splitted_string[0] == "ATL" or splitted_string[0] == "IAD" or splitted_string[0] == "BOS"):
            hour = hour -3
            splitted_time[0] = hour
        if(splitted_string[0] == "ORD"):
            hour = hour - 2
            splitted_time[0] = hour
        else:
            if (int(splitted_time[1]) > 30):
                hour = hour + 1
                splitted_time[0] = hour
        line = splitted_string[0] +","+ splitted_string[1] +","+str(splitted_time[0])+":"+str(splitted_time[1])+","+ splitted_string[3]+","+splitted_string[4]
        temp_obj.write(line)
    temp_obj.close()