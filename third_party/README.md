## archives目录

第三方库源码压缩包。

## build目录

编译、安装脚本。

脚本执行顺序：
1. sudo sys_prepare.sh
2. unzip_all.sh # 可重复执行
3. build_all.sh # 编译、安装第三方库，一般执行一次即可。也可以单独执行其中的一个脚本，如；build_nose.sh

## conf目录

third_party.csv: 第三方库版本配置文件。

当第三方库有版本更新时，修改csv文件中的条目，然后运行main.sh。

除紧急bug外，每年的4月和10月例行更新第三方库的版本。

## doc目录

## patch目录

对第三方库的一些修改。

编译之前要拷贝到第三方库的源码目录。
