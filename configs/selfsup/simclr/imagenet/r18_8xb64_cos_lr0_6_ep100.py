_base_ = '../../_base_/datasets/imagenet/simclr_sz224_bs64.py'

# model settings
model = dict(
    type='SimCLR',
    backbone=dict(
        type='ResNet_mmcls',
        depth=18,
        num_stages=4,
        out_indices=(3,),  # no conv-1, x-1: stage-x
        norm_cfg=dict(type='SyncBN'),
        style='pytorch'),
    neck=dict(
        type='NonLinearNeck',  # SimCLR non-linear neck
        in_channels=512, hid_channels=2048, out_channels=128,
        num_layers=2,
        with_avg_pool=True),
    head=dict(type='ContrastiveHead', temperature=0.1)
)

# interval for accumulate gradient
update_interval = 1  # SimCLR cannot use grad accumulation, total: 8 x bs64 = bs512

# optimizer
optimizer = dict(
    type='LARS',
    lr=0.3 * 2,  # lr=0.3 / bs256
    momentum=0.9, weight_decay=1e-6,
    paramwise_options={
        '(bn|ln|gn)(\d+)?.(weight|bias)': dict(weight_decay=0., lars_exclude=True),
        'bias': dict(weight_decay=0., lars_exclude=True),
    })

# apex
use_fp16 = False
fp16 = dict(type='apex', loss_scale=dict(init_scale=512., mode='dynamic'))
# optimizer args
optimizer_config = dict(update_interval=update_interval, use_fp16=use_fp16, grad_clip=None)

# lr scheduler
lr_config = dict(
    policy='CosineAnnealing',
    by_epoch=False, min_lr=0.,
    warmup='linear',
    warmup_iters=10, warmup_by_epoch=True,
    warmup_ratio=1e-5,
)

# runtime settings
runner = dict(type='EpochBasedRunner', max_epochs=100)