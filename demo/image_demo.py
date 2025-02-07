# Copyright (c) OpenMMLab. All rights reserved.
from argparse import ArgumentParser
from mmengine.model import revert_sync_batchnorm
from mmseg.apis import inference_model, init_model, show_result_pyplot
#bm
import torch
import poptorch
import pdb 


def main():
    parser = ArgumentParser()
    parser.add_argument('img', help='Image file')
    parser.add_argument('config', help='Config file')
    parser.add_argument('checkpoint', help='Checkpoint file')
    parser.add_argument('--out-file', default=None, help='Path to output file')
    parser.add_argument(
        '--device', default='cuda:0', help='Device used for inference')
    parser.add_argument(
        '--opacity',
        type=float,
        default=0.5,
        help='Opacity of painted segmentation map. In (0, 1] range.')
    parser.add_argument(
        '--title', default='result', help='The image identifier.')
    args = parser.parse_args()

    # build the model from a config file and a checkpoint file
    model = init_model(args.config, args.checkpoint, device=args.device)
        
    if args.device == 'cpu':
        model = revert_sync_batchnorm(model)
        
    #bm -----------------------
    from mmseg.apis.inference import _preprare_data
    pdb.set_trace()
    data, is_batch = _preprare_data(args.img, model)
    data2 = model.data_preprocessor(data, False)
    
    opts = poptorch.Options()
    opts.outputMode(poptorch.OutputMode.All)
    pdb.set_trace()
    backbone = poptorch.inferenceModel(model.backbone, opts)
    # feats = backbone(data2['inputs'])    #ok, but need to wait for compiling
    feats = []
    # # feats.append(torch.rand([1, 96, 128, 256]))
    # # feats.append(torch.rand([1, 192, 64, 128]))
    # # feats.append(torch.rand([1, 384, 32, 64]))
    # # feats.append(torch.rand([1, 768, 16, 32]))
    feats.append(torch.rand([1, 96, 144, 288]))
    feats.append(torch.rand([1, 192, 72, 144]))
    feats.append(torch.rand([1, 384, 36, 72]))
    feats.append(torch.rand([1, 768, 18, 36]))
    # # feats.append(torch.rand([1, 96, 144, 144]))
    # # feats.append(torch.rand([1, 192, 72, 72]))
    # # feats.append(torch.rand([1, 384, 36, 36]))
    # # feats.append(torch.rand([1, 768, 18, 18]))
    # # feats.append(torch.rand([1, 96, 144, 144]))
    # # feats.append(torch.rand([1, 192, 72, 72]))
    # # feats.append(torch.rand([1, 384, 36, 36]))
    # # feats.append(torch.rand([1, 768, 18, 18]))
    # # feats.append(torch.rand([1, 96, 96, 96]))
    # # feats.append(torch.rand([1, 192, 48, 48]))
    # # feats.append(torch.rand([1, 384, 24, 24]))
    # # feats.append(torch.rand([1, 768, 12, 12]))
    # feats.append(torch.rand([1, 96, 48, 48]))
    # feats.append(torch.rand([1, 192, 24, 24]))
    # feats.append(torch.rand([1, 384, 12, 12]))
    # feats.append(torch.rand([1, 768, 6, 6]))
    
    pdb.set_trace()
    decode_head = poptorch.inferenceModel(model.decode_head, opts)
    seg_logits = decode_head(feats)
    from mmseg.models.decode_heads.decode_head import resize
    seg_logits = resize(
        input=seg_logits,
        size=(512, 1024),
        mode='bilinear',
        align_corners=False)
    result = model.postprocess_result(seg_logits, data2['data_samples'])
    result = result[0]
    pdb.set_trace()

    # test a single image
    # result = inference_model(model, args.img)
    
    # show the results
    # show_result_pyplot(model, args.img, result, title=args.title, opacity=args.opacity, draw_gt=False, show=False, out_file=args.out_file)  #bm
    show_result_pyplot(
        model,
        args.img,
        result,
        title=args.title,
        opacity=args.opacity,
        draw_gt=False,
        show=False if args.out_file is not None else True,
        out_file=args.out_file)

    pdb.set_trace()

if __name__ == '__main__':
    main()
