# FLAG:RITSEC{AR3_Y0U_F3371NG_1T_N0W_MR_KR4B5?!}
# UklUU0VDe0FSM19ZMFVfRjMzNzFOR18xVF9OMFdfTVJfS1I0QjU/IX0= base 64 in Stars.html linked from Fl4gggg1337.html by a !
import urllib.request 

def gets_url_lists(url,exp):
    f = urllib.request.urlopen(url)
    page1=str(f.read())
    page1=page1.replace("\\n","\n")
    for line in page1.split():
        if "flag" in line.lower():
            print(line)
            print(page1)
            exit()
        if "href" in line:
            line=line.replace("href=\"","")
            line=line[:-1]
            if not line in [a[0] for a in exp]:
                exp.append([line,0])
            




if __name__=="__main__":
    url="http://fun.ritsec.club:8007"
    list_link=[]
    gets_url_lists(url,list_link)
    while True:
        list_link_wb=[ b for b in list_link if b[1]==0 ]
        list_link_wb[0][1]=1
        gets_url_lists(url+"/"+list_link_wb[0][0],list_link)
        print(list_link_wb)
        if not list_link_wb:
            break
