import os
import re

cwd=os.getcwd()

f=open("Action.c")

snaps=[]
corr={}
names={}
ignore=0
snaps_upto={}
comment=0
for i in f:
    if("web_add_auto_header" in i or "XMLHttpRequest" in i):
        continue
    if (ignore==1 or "LAST" in i):
        if("LAST" in i):
            ignore=0
        else:
            continue
    elif("EXTRARES" in i):
        ignore=1
        continue
    if "Snapshot=" in i:
        snap='\\data\\'+(re.findall('Snapshot=(.+?).inf',i)[0])
        if snap not in snaps:
            snaps.append(snap)
    if comment==0 and ('web_url("' in i or 'web_submit_data("' in i or ("start_tran" in i and "ACTION" not in i)):
        start_trans=i[:-3].strip()
        comment=1
    if comment==1 and "LAST;" in i:
        comment=0
        trans_snap[start_trans]=snap.split('\\')[2]
    if "Value" in i:
        try:
            value=re.findall('Value=(.+?)"',i)[0]
            if(len(value) in range(4,41) and value not in corr and re.search('\d',value)):
                name=re.findall('Name=(.+?)"',i)[0].split("-")[-1]
                found=0
                for temp in corr:
                    if name in corr[temp]:
                        names[name]+=1
                        name=name+str(names[name])
                        found=1
                        break
                if found==0:
                    names[name]=0
                    corr[value]=name
                    snaps_upto[value]=len(snaps)
        except:
            continue

f.close()

corr_at={}
replaces={}
for path in snaps:
    try:
        f=open(cwd+path+'.json')
        
    except:
        try:
            f=open(cwd+path+'.html')

        except:
            try:
                f=open(cwd+path+'.htm')
            except:
                continue
    try:
        for lines in f:
            new_dic=corr.copy()
            for cor in corr:
                if snaps.index(path)<snaps+upto[cor]-1 and cor in lines:
                    replaces[cor]=corr[cor]
                    index=lines.index(cor)
                    while True:
                        if cor in lines[index+len(cor):]:
                            index=index+len(cor)+lines[index+len(cor):].index(cor)
                        else:
                            break
                        if path.split('\\')[2] not in corr_at:
                            corr_at[path.split('\\')[2]]={}
                        temp_corr='web_reg_save_param("dyn_'+corr[cor]+'","LB='+lines[index-50:index]+'","RB='+lines[index+len(cor):index+len(cor)+10]+'",LAST);'
                        corr_at[path.split('\\')[2]][corr[cor]]=[lines[index-100:index+50],temp_corr]
                        del new_dic[cor]
            corr=new_dic
    except:
        continue
    f.close()


'''
for i in corr_at:
    print(i)
    for ii in corr_at[i]:
        print(ii)
        print(corr_at[i][ii][0])
        print(corr_at[i][ii][1])
        print()
print(replaces)
'''


os.rename("Action.c","Action-old.c")
reader=open("Action-old.c")
writer=open("Action.c",'w')

thinktime="\tlr_think_time(3);\n"
ignore=0
comment=0
for i in reader:
    if("web_add_auto_header" in i or "XMLHttpRequest" in i):
        continue
    if(ignore==1 or "LAST" in i):
        if ("LAST" in i):
            ignore=0
        else:
            continue
    elif("EXTRARES" in i):
        ignore=1
        continue
    if "think_time" in i:
        writer.write(thinktime)
        continue
    elif comment==0 and (('web_url("' in i or 'web_submit_data("' in i) or ("start_tran" in i and "ACTION" not in i)):
        writer.write('\tweb_reg_find("Text=a","SaveCount=PassCount",LAST);\n')
        writer.write('\tweb_reg_find("Text=a","SaveCount=PassCount1",LAST);\nn')

        if i[:-3].strip() in trans_snap:
            p=trans_snap[i[:-3].strip()]
            if p in corr_at:
                for cor in corr_at[p]:
                    print(corr_at[p][cor][0])
                    print(corr_at[p][cor][1])
                    writer.write('\t//'+corr_at[p][cor][0]+'\n')
                    writer.write('\t'+corr_at[p][cor][1]+'\n')
                print()
                writer.write('\n')

        writer.write(i)
        comment=1
        continue

    elif comment==1 and "LAST);" in i:
        comment=0
        writer.write(i)
        writer.write('\tif((atoi(lr_eval_string("{PassCount}"))==0 || (atoi(lr_eval_string("{PassCount1}"))==0))\n\t{\n')
        writer.write('\tlr_fail_trans_with_error("Error");\n')
        writer.write('\tlr_exit(LR_EXIT_MAIN_ITERATION_AND_CONTINUE,LR_FAIL);\n\t}\n')



    elif "Value" in i:
        try:
            value=re.findall('Value=(.+?)"',i)[0]
            if len(value) in range(4,41) and value in replaces:
                s=str(i)
                s=s.replace(value,'{dyn_'+replaces[value]+'}')
                write.write(s)
            else:
                writer.write(i)
        except:
            writer.write(i)
            continue
    else:
        writer.write(i)

reader.close()
writer.close()

        
        
                                                            








































                        





















        




























        
