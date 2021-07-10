# ace2005chinese_preprocess
ACE 2005 corpus preprocessing for Event Extraction task

## Prerequisites

1. 准备 **ACE 2005数据集**

   (Download: https://catalog.ldc.upenn.edu/LDC2006T06. Note that ACE 2005 dataset is not free.)

2. 安装依赖包
   ```
   pip install beautifulsoup4 nltk tqdm
   ```
3. data_list.csv是需要处理的文件名称，这里我按文档划分为：train.json,dev.json,test.json

## 使用方法

Run:

```bash
python main.py --data=./data/ace_2005/Chinese   #更改成你的数据集位置
``` 


### Format

我遵循nlpcl lab/ace2005预处理中描述的json格式
 [[github]](https://github.com/nlpcl-lab/ace2005-preprocessing)
但目前只有句子，事件，实体，其他信息，如依赖树，pos\u标签等，稍后会添加。实验中随机选择的数据划分方法（data_list.csv）不属于ED任务的权威划分方法。
如果您想详细了解事件类型和参数，请阅读[this document (ACE 2005 event guidelines)](https://www.ldc.upenn.edu/sites/www.ldc.upenn.edu/files/english-events-guidelines-v5.4.3.pdf).

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

