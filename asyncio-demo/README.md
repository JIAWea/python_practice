

### 事件循环
> 事件循环会运行异步任务和回调，执行网络 IO 操作，以及运行子进程

#### start_server
> 启动套接字服务 start_server(client_connected_cb, host, port, ...)
- 当一个新的客户端连接被建立时，回调函数 client_connected_cb 会被调用，该函数会接收到一对参数 `reader, writer` 
    - `reader` 是 StreamReader 的实例
    - `writer` 是 StreamWriter 的实例
    - client_connected_cb 即可以是普通的可调用对象也可以是一个 协程函数; 如果它是一个协程函数，它将自动作为 Task 被调度。

#### open_connection
> 建立网络连接并返回一对 `reader, writer` 对象

#### StreamReader
- read 方法
    - 至多读取 n 个byte。 如果没有设置 n , 则自动置为 -1 ， -1时表示读至 EOF 并返回所有读取的byte。没数据则返回空 bytes 对象


#### StreamWriter
- write 方法
    - 配合 drain 方法使用
- close 方法
    - 配合 wait_closed 方法使用


### Future
> 一个 Future 对象代表一个异步运算的最终结果。线程不安全。
- 例如作为参数传给一个另一个协程，然后协程通过 set_result 方法返回结果。
  ```Future
  
  async def set_after(fut, delay, value):
      # Sleep for *delay* seconds.
      await asyncio.sleep(delay)
  
      # Set *value* as a result of *fut* Future.
      fut.set_result(value)
  
  async def main():
      # Get the current event loop.
      loop = asyncio.get_running_loop()
  
      # Create a new Future object.
      fut = loop.create_future()
  
      # Run "set_after()" coroutine in a parallel Task.
      # We are using the low-level "loop.create_task()" API here because
      # we already have a reference to the event loop at hand.
      # Otherwise we could have just used "asyncio.create_task()".
      loop.create_task(
          set_after(fut, 1, '... world'))
  
      print('hello ...')
  
      # Wait until *fut* has a result (1 second) and print it.
      print(await fut)
  
  asyncio.run(main())
  ```
  
- 调用方接收到结果后可以使用 add_done_callback 方法来使用回调函数，并可通过 functools.partial 方法给回调函数传递参数。
  ```callback

  # Call 'print("Future:", fut)' when "fut" is done.
  fut.add_done_callback(
      functools.partial(print, "Future:"))

  ```


### 协程
> 
- 协程需要通过 loop 循环事件调度
- 在运行的协程中可以等待另一个协程 （await）


### Task
> 一个与 Future 类似 的对象，可运行 Python 协程。非线程安全。
- 使用 create_task 或 ensure_future 方法来创建一个 Task。
  - loop.create_task() == <version 3.7> asyncio.create_task()
- 使用 cancel 方法可以取消一个 Task。
- Task 对象被用在 loop 中运行一个协程。如果运行中的协程在等待一个 Future 对象，Task 则会被挂起，直到等待的协程执行完成。


### 协程与任务

#### 可等待对象
> 协程, Task, Future
- gather(*aws, ...) 方法
    - 并发运行 aws 序列中的 可等待对象。


### 队列集
