import numpy as np
import matplotlib.pyplot as plt

# activate function
def step_func(y):
    if y>0:
        return 1
    return 0

# loss function

def loss(y, t):
    #return 0.5 * (np.sum(y-t)**2)
    return 0.5*(y-t)

class Neuron :
    def __init__(self, input_len):
        #self.x = np.zeros(input_len) # input_vec
        self.b = np.random.rand(1)[0] # bias
        self.w = np.random.rand(input_len) # weight

    def predict (self, x):
        self.x = x
        self.h = np.dot(self.x, self.w)-self.b # sigma(W[n]*X[n])+bias
        self.y = step_func(self.h)
    
    def back_prop (self, t):
        # t: teach_vec
        self.loss = loss(self.y, t)
        self.dw = self.x*self.loss
        self.w = self.w - self.dw
        self.b += self.loss
        

class MatchLearning :
    def __init__(self, max_price, sweets_list):
        self.max_price = max_price
        self.sweets_list = sweets_list
        
        self.sweets_type_num = len(sweets_list)
        
        self.neuron = Neuron(len(sweets_list))
        self.price_list = list(map(lambda cons : cons[1], sweets_list))

    
    def predict(self, input_vec):
        return self.neuron.predict(input_vec)

    def back_prop(self, t):
        return self.neuron.back_prop(t)


    def input_vec_random(self, max_purchase_num=15):
        return np.random.randint(max_purchase_num,size=self.sweets_type_num)
    
    def teach_vec(self, x) :
        return 1 * (np.dot(x, self.price_list) > self.max_price)


    def print_status(self, num=None):
        neu = self.neuron
        t = self.teach_vec(neu.x)

        print("======= num_train:%d =========="% num)
        print("data\t:: price:%s"
                  % np.dot(neu.x, self.price_list))
        print("predict\t:: x:%s w:%s b:%s,\n\t h:%s y:%s"
                  % (neu.x,neu.w,neu.b, neu.h, neu.y))
        print("teach\t:: t:%s error:%s dw:%s"
                  % (t, loss(t, neu.y), neu.dw))
        
    def train1(self, x):
        self.predict(x)
        self.back_prop(self.teach_vec(x))
        
    def plot_result(self):
        plt.plot(self.error_ave)
        plt.show()

        plt.plot(self.dw_list)
        plt.show()

        plt.plot(self.w_list)
        plt.show()
        
        
    def train(self, learn_par_epoch=5, train_num = 10000):
        self.error_ave = []
        self.dw_list = []
        self.w_list = []
        
        for epoch in range(train_num):
            error=0
            
            for i in range(learn_par_epoch):
                x = self.input_vec_random()
                self.train1(x)


                
                error += loss(self.neuron.y, self.teach_vec(x))
                
                #self.print_status(num=epoch)
            self.error_ave = self.error_ave + [error/learn_par_epoch]
            self.dw_list = self.dw_list + [self.neuron.dw ]
            self.w_list = self.w_list + [self.neuron.w]
            
        self.plot_result()    


        

if __name__ == "__main__":
    sweets_list = [("candy", 40), ("chocolate", 80)]#, ("cookie", 200)]
    match_learning = MatchLearning(1000 , sweets_list)
    
    match_learning.train()
    

