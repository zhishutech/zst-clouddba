# snapshot

## 一、触发条件
- thread running
- user cpu/sys cpu超过10%
- iowait超过5%
- 锁等待
- ...
- 或者不指定触发条件

## 二、基础信息收集
- 硬件部分
    - CPU
    - 磁盘
    - 阵列卡
    - 网卡
    - 内存

- 操作系统
    - 操作系统版本
    - 内核版本
    - IO schedule
    - numa
    - 文件系统
    - 操作系统限制
    - selinux
    - swap

## 三、状态信息收集
- variables
- status
- innodb status
- slave status
- processlist
- transactions
- lock info
- error log
- slow log
- message
- dmseg
- top
- iostat
- mpstat
- tcpdump
- disk
- mem info
- interrupts
- ps
- netstat
- vmstat

## 四、文件输出
- time_variables
- time_status
- time_innodb_status
- time_slave_status
- time_processlist
- time_transactions
- time_error_log
- time_slow_log
- time_message
- time_dmseg
- time_top
- time_df
- time_df_space
- time_diskstat
- time_iostat
- time_interrupts
- time_meminfo
- time_mpstat
- time_tcpdump
- time_lock_info
- time_lock_waits
- time_hardware_info
- time_system_info


## 五、输出格式
- 文本格式（本地分析）
- json格式（zst-cloud dba分析）

