# ACE 2005语料库中文信息抽取

## 准备工作
1. 准备 **ACE 2005数据集**

   (Download: https://catalog.ldc.upenn.edu/LDC2006T06)

2. 安装依赖包
   ```
   pip install bs4 nltk tqdm
   ```
3. data_list.csv是需要处理的文件名称，这里我按文档划分为：train.json,dev.json,test.json

## 使用方法

Run:

```bash
python main.py --data=./data/ace_2005/Chinese   #更改成你的数据集位置
``` 


### 格式

我遵循nlpcl lab/ace2005预处理中描述的json格式
 [[github]](https://github.com/nlpcl-lab/ace2005-preprocessing)
但目前只有句子，事件，实体，其他信息，如依赖树，pos\u标签等，稍后会添加。实验中随机选择的数据划分方法（data_list.csv）不属于ED任务的权威划分方法。

### 处理示例
**`sample.json`**
```json

[
   {
    "sentence": "美国《华盛顿邮报》：美国共和党总统候选人小布什放弃海外军人选票诉讼案",
    "position": [
      94,
      130
    ],
    "golden-entity-mentions": [
      {
        "text": "美国《华盛顿邮报",
        "phrase-type": "NAM",
        "position": [
          94,
          102
        ],
        "entity-type": "ORG:Media"
      },
      {
        "text": "美国",
        "phrase-type": "NAM",
        "position": [
          94,
          96
        ],
        "entity-type": "GPE:Nation"
      },
      {
        "text": "美国",
        "phrase-type": "NAM",
        "position": [
          105,
          106
        ],
        "entity-type": "GPE:Nation"
      },
      {
        "text": "小布什",
        "phrase-type": "NAM",
        "position": [
          115,
          117
        ],
        "entity-type": "PER:Individual"
      },
      {
        "text": "美国共和党总统候选人",
        "phrase-type": "NOM",
        "position": [
          105,
          114
        ],
        "entity-type": "PER:Individual"
      },
      {
        "text": "美国共和党",
        "phrase-type": "NAM",
        "position": [
          105,
          109
        ],
        "entity-type": "ORG:Non-Governmental"
      },
      {
        "text": "总统",
        "phrase-type": "NOM",
        "position": [
          110,
          111
        ],
        "entity-type": "PER:Individual"
      },
      {
        "text": "海外军人",
        "phrase-type": "NOM",
        "position": [
          120,
          123
        ],
        "entity-type": "PER:Group"
      },
      {
        "text": "海外",
        "phrase-type": "NOM",
        "position": [
          120,
          121
        ],
        "entity-type": "LOC:Region-International"
      }
    ],
    "golden-event-mentions": [
      {
        "trigger": {
          "text": "诉讼",
          "position": [
            127,
            128
          ]
        },
        "arguments": [
          {
            "role": "Defendant",
            "position": [
              115,
              117
            ],
            "entity-type": "PER:Individual",
            "text": "小布什"
          }
        ],
        "position": [
          127,
          128
        ],
        "event_type": "Justice:Sue"
      }
    ]
  },
]
```

## 后期工作，根据需要进一步添加词性、语法树等处理。