#!/usr/bin/env python
# -*- coding: UTF-8 -*-  

'''
{
"版权":"LQAB工作室",
"author":{
"1":"腾辉",
"2":"吉更"
"3":"MLtf"
}
"初创时间:"2017年3月",
}
'''

# ---系统参变量处理
import re # 正则模块
import sys
sys.path.append("..")
import config #导入系统配置参数模块


#-----系统外部需安装库模块引用-----
user_dic_path = config.dic_config["path_jieba_dic"]
import jieba # 引入结巴分词类库 第三方库
jieba.default_logger.setLevel('ERROR') #结巴分词 自动纠错
import jieba.posseg as pseg #引入词性标注模式
jieba.load_userdict(user_dic_path)# 导入专用字典

# nlp基础类

class Nlp_base(object):

    # 自然分段
    def nature_paragraph(self,txt_p="",list_p=[],ignore_list=[]):
        
        if (len(list_p) == 0):
        
            list_p = [
            "'",
            "\n",
            "\"",
            ",",
            "（",
            "）",
            "(",
            ")",
            "，",
            "。",
            "；",
            "“",
            "”",
            "（",
            "）",
            "？",
            "：",
            "《",
            "》",
            "『",
            "』",
            "[",
            "]",
            "！",
            "、",
            "\\",
            "=",
            "×",
            "÷",
            "+",
            "-",
            "≈",
            "【",
            "】",
            "〖",
            "〗",
            "[",
            "]",
            "｛",
            "｝",
            "?",
            "±",
            "/",
            "≌",
            "∽",
            "∪",
            "∩",
            "∈",
            "\r\n", 
            "\n",
            "\r",
            " ",
            "  ",
            "|",
            "_",
            ]
        
        # 利用标点和特殊符号分段
        for x in list_p:
            txt_p = txt_p.replace(x,"\n" + x + "\n")
        
        # 停用词初滤
        for x in ignore_list:
            txt_p = txt_p.replace(x,"")
        
        return txt_p
         
# 分词
class Segment(Nlp_base):

    def __init__(self,txt_p="",threshold_p=0,way_p="precise"):
    
        self.txt_p = txt_p
        self.threshold_p = threshold_p
        self.way_p = way_p
        
    # 结巴分词转列表
    def jieba2list(self,token_p=""):
        list_last = []
        for x in token_p:
            list_last.append(x)
        return list_last
        
    # 自然分段
    
    def section_nature(self,txt_p):
        pass
        
    # 自然分词
    def seg_nature(self):
        pass

    # 结巴中文分词
    def seg_jieba(self,txt_p="",way_p=""):
        
        if (txt_p == ""):
            txt_p = self.txt_p
        
        if (way_p == ""):
            way_p = self.way_p
        
        list_p = []

        if (len(txt_p) == 0):
            return list_p
        
        #  搜索引擎模式
        if (way_p == "search"):
            try:
                list_p = jieba.cut_for_search(txt_p)
            except:
                list_p = []
                
        # 默认 精确模式   
        if (way_p == "precise"):
        
            try:
                list_p = jieba.cut(txt_p)
            except:
                list_p = []
                
        # 全模式   
        if (way_p == "all"):
            try:
                list_p = jieba.cut(txt_p,cut_all=True)
            except:
                list_p = []
            
        return list_p
        
    # 词性标注分词
    def seg_pseg(self,txt_p=""):
        list_p = []
        str_t = ""
        if (txt_p ==""):
            words = pseg.cut(self.txt_p)
        else:
            words = pseg.cut(txt_p)
        for word,flag in words:
            str_t = "['" + word + "','" + flag + "']"
            list_p.append(str_t)
        #print(list_p) #调试用
        return list_p
        
    # 主分词方法 threshold_p 主处理入口参数 way_p 后续处理入口参数
    def seg_main(self,txt_p="",threshold_p=0,way_p="precise"):
        
        list_s = []
        str_t = ""
        list_last = []
        list_t = []
    
        if (txt_p == ""):
            txt_p = self.txt_p
            
        if (threshold_p == ""):
            threshold_p = self.threshold_p
        
        if (way_p == ""):
            way_p = self.way_p
            
        # 按处理入口选择性处理
        
        # 调用结巴模块的标准分词 匹配模块常用
        if (threshold_p == 0):
            list_t = self.seg_jieba(txt_p=txt_p)
            for y in list_t:
                list_last.append(y)
        
        # 引入自然分词 + 结巴 新词识别模块常用
        if (threshold_p == 1):

            # 自然分段
            str_t = self.nature_paragraph(txt_p)
            list_s = str_t.split("\n")
            for x in list_s:
                if (len(x) < 2):
                    list_last.append(x)
                else:
                
                    # 自然分词的阈值判别
                    if (len(x) <= config.dic_config["numb_nature_segment"]):
                        list_last.append(x)
                    else:
                        # 标准分词
                        list_t = self.seg_jieba(txt_p=x)
                        for y in list_t:
                            list_last.append(y)
        
        return list_last

    # 自定义字典切词分词
    def segment_dic_cut(self,txt_p="",dic_p={},action_p="left",step_p=6,end_p=1):
        txt = txt_p
        list_p = []
        
        if (len(txt) <= step_p):
            list_p.append(txt)
            return list_p #小于切词步阈长度直接返回
        
        # 由左到右正向分词
        if (action_p == "left"):
            s=0
            e=step_p
            while (s < len(txt_p)-1-end_p):
                str_t = txt[s:e]
                for i in range(step_p-1):
                    if str_t in dic_p:
                        list_p.append(str_t)
                        s += i + 1
                        break
                    else:
                        str_t = str_t[s:e-i]
                        if (e-i == end_p):
                            list_p.append(str_t)
                            s += end_p
                            break
        
        # 由右到左逆向分词
        if (action_p == "right"):
            s=0
            e=step_p
            while (s > -1*(len(txt_p)-1-end_p)):
                str_t = txt[-1*e:-1*s]
                for i in range(step_p-1):
                    if str_t in dic_p:
                        list_p.append(str_t)
                        s += -1*(i + 1)
                        break
                    else:
                        str_t = str_t[-1*(e-i):s]
                        if (-1*(e-i) == end_p):
                            list_p.append(str_t)
                            s += -1*end_p
                            break
        
        return list_p
        
# 相似度类
class Similar(object):

    # 比对词向量的构造
    def vector_cos_word(self,list_v1=[],list_v2=[]):
        
        list_v1_out = []
        list_v2_out = []
        list_b = list_v1 + list_v2
        list_s = sorted(set(list_b),key=list_b.index) # 去重排序
        
        #print(list_s,"\n",list_v1,"\n",list_v2) # 调试用
        
        for x in list_s:
        
            list_v1_out.append(list_v1.count(x))
            list_v2_out.append(list_v2.count(x))
                
        #print(list_s,list_v1_out,list_v2_out) # 调试用
                
        return list_v1_out,list_v2_out
            
    
    # 词向量余弦相似度计算
    def cos_word(self,sim_1=[],sim_2=[]):
    
        sim_value = -1 # 相似度值赋初值 1 完全相似 -1 完全相反
        epsilon = 10e-10
        pow_1 = 0
        pow_2 = 0
        inner_product = 0
        list_em = []  # 标准向量
        import math
        
        sim_1,sim_2 = self.vector_cos_word(list_v1=sim_1,list_v2=sim_2)
        #print(sim_1,sim_2)
        for i in range(len(sim_1)):
            #print(i) # 调试用
            inner_product += sim_1[i] * sim_2[i]
            pow_1 += sim_1[i]**2
            pow_2 += sim_2[i]**2
        #print ("inner_product=",inner_product**2,"pow_1*pow_2=",pow_1*pow_2)
        sim_value = round(inner_product/(math.sqrt(pow_1*pow_2)+epsilon),10) # 保留小数点后10位
        
        return sim_value

# 文本抽取类
class Extract_txt(object):

    #对文本按自然段分段 mark_p 为自然分段标记符列表
    def div_cut(self,content_p="",mark_p=["']\"","</p>","</div>"]):
    
        list_t = []
        
        # 自然分段标记处理
        for x in mark_p:
            content_p = content_p.replace(x,"\n")
            
        content_p = content_p.replace("\r\n","\n")
        #print (content_p.count("\n")) # 调试用
        list_t = content_p.split("\n")
        
        return list_t

    #对含标点的文本分句
    def sentence_cut(self,content_p,father_if=1):
    
        import  re # 引用正则库
        # 主句与子句分割
        
        if (father_if == 1):
            cutlist =['。','？','！']
        else:
            cutlist =['，','；','：','”']
            
        content_p = content_p.replace("["," ")
        content_p = content_p.replace("]"," ")
        content_p = content_p.replace("'"," ")
        content_p = content_p.replace("\""," ")
            
        # 对汉语标点符号的错误进行纠正
        if (father_if == 1):
            content_p = content_p.replace("?","？")
            content_p = content_p.replace("!","！")
        else:
            content_p = content_p.replace(":","：")
            
        pat = re.compile('\s+')
        content_p=re.sub(pat,'',content_p)
        
        bst=[content_p]
        est=[]
        
        for flag in cutlist:
            for a in bst:
                est.extend(a.split(flag))
            bst,est=est,[]
            
        return bst
        
    # 获得自然段——主句映射字典
    def sentence_div_main_get(self,content_p=""):
        
        dic_div ={} # 自然段落字典
        dic_sen_main = {} # 主句字典
        list_t = [] # 临时队列
        list_t = self.div_cut(content_p=content_p) # 自然段分段
        #print ("分段结果：",len(list_t))
        i = 1
        for x in list_t:
            dic_div[i] = x
            i +=1
        j = 1
        # 主句分割 并建立在字典建立索引
        while (j < i):
            list_t = []
            #print(j,dic_div[j]) #调试用
            list_t = self.sentence_cut(dic_div[j],father_if=1)
            #print ("自然段的主句切割：",list_t,type(list_t)) # 调试用
            dic_sen_main[j]=list_t
            j += 1
            
        return dic_sen_main
        
# 自然语言处理基类
class Nlu_base(object):
        
    pass
    
# 自然语言处理主类
class Nlu(Nlu_base):
    
    def __init__(self):
    
    # 内嵌的主要参数型数据
        self.list_feeling = [
        "嘛",
        "吗",
        "呢",
        "哦",
        "么",
        "麽",
        "啊",
        "呀",
        "哪",
        "吧",
        "啦",
        "喽",
        "谁",
        "啥",
        "咋"
        ]
        self.list_query = [
        "什么",
        "难道",
        "究竟",
        "怎的",
        "怎样",
        "怎么",
        "如何",
        "多长",
        "多大",
        "多小",
        "多差",
        "多少",
        "多好",
        "多坏",
        "多久",
        "有何",
        "几斤",
        "几天",
        "几月",
        "几秒",
        "几分",
        "几时",
        "几日",
        "几年",
        "可否",
        "能否",
        "是否",
        "有无",
        "帮我",
        "能不能",
        "行不行",
        "好不好",
        "有没有",
        "是不是",
        "大不大",
        "会不会",
        "可不可以",
        "严不严重",
        "成不成",
        "需不需要"
        ]
        self.list_field = [
        "请问",
        "请帮",
        "请求",
        "寻求",
        "疑似",
        "疑是",
        "咨询",
        "请教",
        "想问"
        ]
        self.list_head = [
        "求",
        "寻找",
        "帮帮",
        "怀疑",
        "关于",
        "想知道"
        ]
        self.list_foot = [
        "区别",
        "办法",
        "问题",
        "疑问",
        "的是",
        "值是",
        "是指",
        "这是",
        "数是",
        "的原因",
        "的表现",
        "调理",
        "费用",
        "事项",
        "几率",
        "概率",
        "症状",
        "治疗方案",
        "治疗手段",
        "临床表现",
        "的预后",
        "饮食",
        "治疗",
        "症状",
        "方法",
        "情况",
        "先兆",
        "程度",
        "的关系",
        "的危害",
        "药方",
        "药物",
        "食疗",
        "偏方",
        "疗法",
        "方案",
        "效果"
        ]
        self.list_regular = [
        "是.*?还是",
        "除了.*?还有",
        "有.*?没",
        "有.*?不",
        "解答.*?下",
        "求.*?帮忙",
        "问.*?下",
        "得到.*?帮助"
        ]
    
    # 问题识别决策树法
    def question_if_tree(self,str_p="",list_feeling=[],list_query=[],list_field=[],list_head=[],list_foot=[],list_regular=[]):
        
        list_t = [] # 临时队列
        
        # 决策树匹配集处理
        if (list_feeling == []):
            list_feeling = self.list_feeling
        if (list_query == []):
            list_query = self.list_query
        if (list_field == []):
            list_field = self.list_field
        if (list_head == []):
            list_head = self.list_head
        if (list_foot == []):
            list_foot = self.list_foot
        if (list_regular == []):
            list_regular = self.list_regular
            
        result_p = 0
        
        #决策节点0 存在疑问标点
        if ("？" in str_p or "?" in str_p):
            result_p = 1
            return result_p
        #决策节点1 存在疑问助词
        for x in list_feeling:
            if (x in str_p):
                result_p = 1
                return result_p
        #决策节点2 存在疑问代词
        for x in list_query:
            if (x in str_p):
                result_p = 1
                return result_p
        #决策节点3 存在领域疑问词
        for x in list_field:
            if (x in str_p):
                result_p = 1
                return result_p
        #决策节点4 存在头部关键词
        for x in list_head:
            if (x == str_p[:len(x)]):
                result_p = 1
                return result_p
        #决策节点5 存在尾部关键词
        for x in list_foot:
            if (x == str_p[len(str_p)-1*len(x):]):
                result_p = 1
                return result_p
        #决策节点6 正则判别
        for x in list_regular:
            list_t = []
            list_t = re.finditer(x,str_p)
            for y in list_t:
                if (str(y) != ""):
                    result_p = 1
                    return result_p
                
        return result_p
    
    # 问题识别主函数
    def question_if_is(self,str_p=""):
        
        #1 规则决策树法处理
        result = self.question_if_tree(str_p=str_p)
        return result_p
        
#---------- 主过程<<开始>> -----------#
def main():

    print ("")  # 防止代码外泄 只输出一个空字符

if __name__ == '__main__':
    main()
#---------- 主过程<<结束>> -----------#