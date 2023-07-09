# Owel Tool

本项目为 OpenSODA 大赛的 **T2：命令行交互的指标结果查询子模块** 的提交作品，该工具主要以 `Python` 实现。输入为查询条件，在命令行显示查询结果并导出至`.csv` 文件。

### 1. 工具设计



#### 【输入】
目前，此工具的基本输入为 `指标名`，`仓库名` 以及 `时间范围`：
- `指标名`：输入为一组指标名（可以为单指标），具体包括：
  - 泛化指标名 `all`，`x-all`，`c-all` 均代表一组指标名，`all` 为查询目前 OpenDigger 支持的所有指标，`x-all` 对应 X-Lab 作为源的指标名集合，`c-all` 代表 CHAOSS 指标名集合
  - 单指标名，例如 `openrank`
  - 多指标名，例如 `(openrank, stars)`
- `时间范围`：时间范围有三种：
  - 闭区间：例如 `[2022-02, 2022-06]`
  - 单时间点：例如 `2022-06`
  - 离散时间点：例如 `(2022-02, 2022-05, 2021-09)`
- `仓库名`：仓库名可以指 用户 或 仓库，需要用户自己判别。例如某些指标是不支持用户级别的查询的，在目前版本没有对此类情况的处理。


#### 【输出】
- CLI 显示
- 导出为 `.csv` 文件，以时间戳记录本次查询结果；
- 导出为 `.html` 文件，渲染更为美观（TODO）

#### 【概要设计】

![基本思想](png/queryowel-design.png)


### 2. 使用说明

1. 首先安装本项目运行所需的依赖
```python
pip install -r requirements.txt
```
2. 运行 `owel.py`，启动前输入的参数将作为全局缺省默认参数：
```python
python src/owel.py [--repo=] [--month=] [--metric=]
```
，将以默认参数执行


【示例 1】全局设置默认参数，后续在未输入具体值的选项会自动走全局值

```python
python owel.py --month="2022-02" --metric="openrank" --repo="lroethan"
Repository Name: 
Metric Name: 
Month: 

Repo.name = lroethan
+------------+------------+------------+
| Metric     | Month      | Value      |
+------------+------------+------------+
| openrank   | 2022-02    | No data    |
+------------+------------+------------+
```

【示例 2】使用泛化时间参数 `-`，将查询所有月份。
```python
Repository Name: lroethan
Metric Name: openrank
Month: -

```

【示例 3】使用泛化指标名，例如 `x-all`，`c-all`，`all`，使用离散时间点 `(2022-04, 2022-05, 2022-06）`
```python
Repository Name: lroethan
Metric Name: x-all
Month: (2022-04, 2022-05, 2022-06)

Repo.name = lroethan
+------------+------------+------------+
| Metric     | Month      | Value      |
+------------+------------+------------+
| openrank   | 2022-04    | 1.25       |
+------------+------------+------------+
| openrank   | 2022-05    | 1.1        |
+------------+------------+------------+
...
```

### 3. 开发说明