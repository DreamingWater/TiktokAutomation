# Drafts In JianYing   | 剪映中的草稿文件一览  
Version:Latest  

### 1.0 阿卡姆剃刀
>　“如无必要，勿增实体”

对于一个商业软件而言,鲁棒性是重要的，在这方面剪映十分优秀.  
对于个人开发者而言,把每个选项都弄明白却不是一个简单的事情，这也不是推荐的方式，所以，在开发时，**没有任何必要**去像官方一样补全所有字段，因为只要你补全所有的必要字段，剪映会帮你把剩下的补全。  

> 资源库≠媒体    

与Pr,FinalCutPro,Davenci等软件不同的是，剪映拥有一套强大的媒体库，本地的媒体和官方的资源调用逻辑完全不同。
### 1.1 草稿位置  
Windows: 安装目录的同一目录下`JianyingPro Drafts.json`中
### 1.2 文件结构(必要)
```
/
    draft_content.json      时间线上的大多数操作
    draft_meta_info.json    资源库中的资源及项目概览
```


### 2.1 `draft_meta_info.json`
该文件记录了资源库中的资源及项目概览,初始结构如下:
![D_empty](https://user-images.githubusercontent.com/32994395/216262271-9d9ce3be-fbcc-4994-b4fd-c167dcb7cf24.png)

#### Root:  
|K|V|Des|
|:--:|:--:|:--:|
|draft_fold_path|`C`:/`xxx`/JianyingPro Drafts/`HelloWorld`|草稿文件夹的地址(Root)|
|draft_cover|`draft_cover.jpg`|草稿文件封面图(相对路径)|
|draft_name|``HelloWorld``|草稿文件名|
|draft_removable_storage_device|`C:`|移动硬盘盘符|
|draft_root_path|`C`:/`xxx`/JianyingPro Drafts/|草稿文件夹父目录路径|
### Root -> draft_materials -> type0 -> value:
媒体信息
![D_EG1](https://user-images.githubusercontent.com/32994395/216268447-a6f3e463-8d1d-4ff2-9574-a169364fc53a.png)
|K|V|Des|
|:--:|:--:|:--:|
|extra_info|`Cat.png`|文件描述名|
|file_Path|`C:/Cat.png`|文件目录|
|metetype|photo|媒体类型(photo,video,music)|
|id|`468c5693-6et0-41b8-b12g-1244dghd2733`|媒体Id|



### 2.2 `draft_meta_info.json`
这是`draft_meta_info.json`的初始结构图,内容复杂,但承载了绝大部分功能
![C_empty](https://user-images.githubusercontent.com/32994395/216267561-078f9b76-4c6f-4e25-84e1-b063db15e73e.png)
### Root:
|K|V|Des|
|:--:|:--:|:--:|
|canvas_config|`{"height":1080,"ratio":"original","width":1920}`|草稿的比率|
|color_space|0|色彩空间|
|fps|30|帧率|

Part1: Materials  
这是记录所有素材、文本、的地方  
#### Effect:特效
|K|V|Des|
|:--:|:--:|:--:|
|apply_target_type|2|必要|
|id|E5E73C6B-8263-4896-957E-8CAB9B044940|id|
|name|蓝色丝印|特效名称|
|resource_id|7131985730791805448|资源id|
|type|video_effect||

Part2: Tracks  
真正的时间线，通过ID和Material进行单向链接  

要补全这个大框架显然是困难的，在实际开发时若希望的功能不存在，使用比较工具把前后内容比对即可得出大多结构，届时欢迎补全本文档。

### 2.3 ID
ID是联系整体的骨架,也是最复杂的地方。  
随机一个新的ID并不复杂，同时只要把这些ID对应的关系联系正确，系统并不会报错。
我们建议使用`UUID`来新建ID.  
对于这些ID，我们分为两类：
- 基于时间建立的ID `(Python：uuid.uuid1())`
- 基于文件建立的ID `(Python: uuid.uuid3(namespace=uuid.namespace,name="xxx"))`

### 2.4 代理设置
项目目录中新建`draft_agency_config.json`,内容如下
```json
{
    "marterials":null,
    "use_converter":true, //是否使用代理 
    "video_resolution":540 // 代理分辨率 540 | 720
}
```
