# model settings
model = dict(
    type='A2MIM',
    backbone=dict(
        type='SimMIMViT',
        arch='deit-small',
        replace=False,  # use residual mask token
        mask_layer=0, mask_token='learnable',
        img_size=192, patch_size=16,
        drop_rate=0., drop_path_rate=0.1,
        use_window=True, init_values=0.1,  # SimMIM: use init_value and relative pos encoding
    ),
    neck=dict(
        type='NonLinearMIMNeck',
        decoder_cfg=None,
        in_channels=384, in_chans=3, encoder_stride=16),
    head=dict(
        type='MIMHead',
        loss=dict(type='RegressionLoss', mode='l1_loss',
            loss_weight=1.0, reduction='none'),
        unmask_weight=0.,
        unmask_replace='mixed',
        fft_weight=0.5,
        fft_focal=True,
        fft_unmask_weight=0.,  # unmask patches in the fft loss
        fft_reweight=False,
        encoder_in_channels=3,
    ))
