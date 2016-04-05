#更改math函数为所需要的函数
'''
蒙特卡洛
        积分        Monte_Carlo_Integral
        直接采样    Monte_Carlo_Direct_Sampling
        接受拒绝采样Monte_Carlo_Acceptance_Rejection_Sample
        重要性采样
'''

from random import *
import math
class Monte_Carlo_Integral:
    start=0
    end=0
    numbers=0
    means=0.0
    var=0.0
    def __init__(self,numbers,start,end):
        self.start=start
        self.end=end
        self.numbers=numbers
    #可以更改为需要的函数
    def function(self,x):
        return math.atan(x)/(x**2+x*math.sin(x))
        #return x**2
    def integral(self):
        array=[0.0 for i in range(self.numbers)]
        a=Random()

        for i in range(self.numbers):
            '''
            非array[i]=self.function(a.uniform(self.start,self.end))*(self.end-self.stop),为了减少乘法运算
            所以在求均值要乘上self.end-self.stop)
                    方差要乘上(self.end-self.stop)*（self.end-self.stop)
          '''
            array[i]=self.function(a.uniform(self.start,self.end))
            self.means+=array[i]
        self.means=(self.means/self.numbers)
        for i in range(self.numbers):
            self.var+=(self.means-array[i])**2

        self.means*=(self.end-self.start)
        self.var*=((self.end-self.start)**2)
        self.var/=self.numbers
        print('Means:',self.means)
        print('Variance:',self.var)
        print('Std Variance:',math.sqrt(self.var/self.numbers))
'''
离散型分布函数 :
    a=[[1,0.25],[2,0.25],[3,0.25],[4,0.25]]
    test=Monte_Carlo_Discrete_Direct_Sampling(a,4)
    test.sample(10)
'''
class Monte_Carlo_Discrete_Direct_Sampling:
    x=[]
    P=[]
    denominator=0
    table=[]
    #要求输入概率分母denominator是一样的，方便制表，分母不一样，需要求最小公倍数，然而这里不想写
    def __init__(self,x_and_p,denominator):
        buff=0
        self.denominator=denominator
        for i in range(len(x_and_p)):
            self.x.append(x_and_p[i][0])
            buff+=x_and_p[i][1]
            self.P.append(buff)
        self.make_table()

    def make_table(self):
        j=0
        for i in range(len(self.x)):
            while True:
                if j<self.P[i]*self.denominator:
                    self.table.append(self.x[i])
                    j+=1
                else:
                    break
    def sample(self,numbers):
        array=[0 for i in range(numbers)]
        a=Random()
        for i in range(numbers):
            array[i]=self.table[int(a.random()*self.denominator)]
        return array
'''
连续型分布函数：
    没写
'''
class Monte_Carlo_Discrete_Continuous_Sampling:
    a=0
class Monte_Carlo_Acceptance_Rejection_Sample:
    start=0
    stop=0
    def __init__(self,start,stop):
        self.start=start
        self.stop=stop
    #可以更改为需要的函数
    #示例用的为正态分布N(1,1)
    def function(self,x):
        mean=1
        s=1#标准差
        if x>self.start and x<self.stop :
            return (math.exp(-((x-mean)**2)/(2*(s**2))))/(s*(math.sqrt(2*math.pi)))
        else :
            return 0
    #更改成函数的积分表达式
    def function_integral_by_input(self):
        #method 1：需要输入函数的积分形式，准确
        #return (self.stop**2-self.start**2)/4
        return 0
    def function_integral_by_monte_carlo(self,times=10000):
        #method 2：利用Monte_Carlo_Integral估计积分结果，不准确
        array=[0.0 for i in range(times)]
        a=Random()
        means=0
        for i in range(times):
            array[i]=self.function(a.uniform(self.start,self.stop))
            means+=array[i]
        means=(means/times)*(self.stop-self.start)
        return (means)

    def function_max_by_input(self,x):
        return self.function(x)
    def function_max_by_monte_carlo(self,times=10000):
        buff=0.0
        max=0.0
        a=Random()
        for i in range(times):
            buff=self.function(a.uniform(self.start,self.stop))
            if buff>max:
                max=buff
        return max

    def sample(self,numbers):
        array=[0.0 for i in range(numbers)]
        #u>=p(x)/(kq(x)),则采样 否则舍弃此采样点
        #u为【0，1】之间随机数 ； p(x)为变量x概率密度；q（x）此处取【0，1】随机数
        k=0.0
        x=0.0
        u=0.0
        a=Random()
        #用Monte Carlo 方法估计p（x）最大值和p（x）在区间【start,stop】的面积
        #如果知道准确值 则用准确值替换function_max_by_monte_carlo和function_integral_by_monte_carlo
        #k=(self.function_max_by_monte_carlo()/self.function_integral_by_monte_carlo())*(self.stop-self.start)           #方法一
        k=(self.function_max_by_monte_carlo()/self.function_integral_by_monte_carlo())/((1)/(2*math.sqrt(2*math.pi)))   #方法二
        for i in range(numbers):
            while True:
                #x=a.uniform(self.start,self.stop)
                x=a.gauss(0,2)
                u=a.random()
                if u<(self.function(x)/(k*(math.exp(-((x-0)**2)/(2*(2**2))))/(2*(math.sqrt(2*math.pi))))):#配套更改
                    array[i]=x
                    break
        return array

#积分测试
#test=Monte_Carlo_Integral(10000,0,1)
#test.integral()

#接受拒绝采样测试
#测试函数 p N(1,1) q N(0,4)
numbers=100000
import numpy as np
import matplotlib.pyplot as plt
import math
class guass:
    mean=0
    s=0
    def __init__(self,mean,s):
        self.mean=mean
        self.s=s
    def function(self,x):
        result=[0 for i in range(len(x))]
        for i in range(len(x)):
            result[i]=(math.exp(-((x[i]-self.mean)**2)/(2*(self.s**2))))/(self.s*(math.sqrt(2*math.pi)))
        return result
x = np.linspace(-4, 4, 10000)
math1=guass(1,1)
math2=guass(0,2)
y = math1.function(x)
z =math2.function(x)
plt.figure(figsize=(8,4))
plt.plot(x,y,label="$N(1,1)$",color="red",linewidth=2)
plt.plot(x,z,"b--",label="$N(0,2)$")
plt.xlabel("Time(s)")
plt.ylabel("Volt")
plt.title("PyPlot First Example")
plt.ylim(0,1)
a=Monte_Carlo_Acceptance_Rejection_Sample(0,4)
data =a.sample(numbers)
bins = np.linspace(-4, 4, 100) #浮点数版本的range
plt.hist(data, bins,normed=1, histtype='stepfilled')
plt.legend()
plt.show()



