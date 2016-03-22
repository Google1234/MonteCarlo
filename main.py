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
    def function(self,x):
        return x/2
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
                if u<(self.function(x)/k*(1/(self.stop-self.start))):
                    array[i]=x
                    break
        return array

test=Monte_Carlo_Integral(10000000,0,1)
test.integral()

'''
Means: 13.138739162029212
Variance: 16739881.177172963
Std Variance: 4.091439988216003

Means: 6.551904940829836
Variance: 177389.1088770188
Std Variance: 0.4211758645471257

Means: 13.203920817423551
Variance: 22765517.720458716
Std Variance: 4.771322428893138

效果并不好怎么办 函数x-->0时，值非常大
'''
