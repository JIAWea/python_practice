### Cold and Hot

#### cold

一个冷被观察者(发布者)会发出一个特定的序列，当有观察者订阅时，它才会开始发出这个序列，并且以观察者希望的任何速度，而不会破坏序列的完整性。可以是：一个数据库查询的结果，文件检索，或网络请求。

#### hot

热被观察者(发布者)，不依赖于订阅者的数量。即使没有订阅者它们也会发出数据， 如果有一个订阅者接入进来，那么它只能收到订阅之后发出的元素。



### 背压

#### throttling 节流
```
sample()/throttleLast()
throttleFirst()
throttleWithTimeout()
```

#### stopAndWait 和 窗口
```
stopAndWait()       # 1
windown(n)
```

#### request n
```
onStart() --> request(n)
onNext()  --> reqeust(n)
```


#### Strategy

> reactor 当下游消费者的 request n 较少时，采用以下策略
1. ERROR
2. DROP
    - LATEST
3. BUFFER       # 有限/无限

#### Comparison

|          | rxpy      | reactor                                            |
| -------- | :-------- | :------------------------------------------------- |
| 背压     | request n | request n                                          |
| 背压策略 |           | 1. error<br />2. drop<br />3. latest<br />4.buffer |

