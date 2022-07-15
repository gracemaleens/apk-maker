import os
import click


@click.group()
@click.pass_context
@click.option('-s', '--src', required=True, help='需要执行命令的apk或包路径')
@click.option('-o', '--out', help='执行命令后的输出路径')
def apkmaker(ctx, src, out):
    ctx.ensure_object(dict)
    
    ctx.obj['src'] = src
    ctx.obj['out'] = out


@apkmaker.command()
@click.pass_context
def decode(ctx):
    src = ctx.obj['src']
    out = ctx.obj['out']
    
    if out is None:
        out = os.path.join(os.path.splitext(src)[0])
    
    cmd = 'apktool d -f "{}" -o "{}"'.format(src, out)
    os.system(cmd)


@apkmaker.command()
@click.pass_context
@click.option('-sign', '--signature', type=click.BOOL, default=True,
              help='构建后执行签名命令')
@click.option('-ks', '--keystore', default='F:\\MixerWorkspace\\honeycomb\\__signfiles\\ngame.jks',
              help='包含私钥和证书的密钥库文件。')
@click.option('-ks-pass', '--ks-pass',
              help='包含签名者私钥和证书的密钥库的密码。')
@click.option('-key-alias', '--key-alias',
              help='密钥库中的私钥和证书数据的别名的名称。')
@click.option('-key-pass', '--key-pass',
              help='私钥的密码，如果与密钥库密码相同，则不需指定')
@click.option('-key', '--key', default='F:\\MixerWorkspace\\honeycomb\\__signfiles\\ngame.pk8',
              help='包含签名者私钥的文件的名称。该文件必须使用 PKCS #8 DER 格式。')
@click.option('-cert', '--cert', default='F:\\MixerWorkspace\\honeycomb\\__signfiles\\ngame.x509.pem',
              help='包含签名者证书链的文件的名称。此文件必须使用 X.509 PEM 或 DER 格式。')
@click.option('-a', '--align', type=click.BOOL, default=True, help='签名后执行对齐命令')
def build(ctx, signature, keystore, ks_pass, key_alias, key_pass, key, cert, align):
    src = ctx.obj['src']
    out = ctx.obj['out']
    
    if out is None:
        out = src + '.apk'
    
    cmd = 'apktool b -f "{}" -o "{}"'.format(src, out)
    os.system(cmd)
    
    if signature:
        ctx.obj['src'] = out
        ctx.invoke(sign, keystore=keystore, ks_pass=ks_pass, key_alias=key_alias, key_pass=key_pass, key=key, cert=cert,
                   align=align)


@apkmaker.command()
@click.pass_context
@click.option('-ks', '--keystore', default='F:\\MixerWorkspace\\honeycomb\\__signfiles\\ngame.jks',
              help='包含私钥和证书的密钥库文件。')
@click.option('-ks-pass', '--ks-pass',
              help='包含签名者私钥和证书的密钥库的密码。')
@click.option('-key-alias', '--key-alias',
              help='密钥库中的私钥和证书数据的别名的名称。')
@click.option('-key-pass', '--key-pass',
              help='私钥的密码，如果与密钥库密码相同，则不需指定')
@click.option('-key', '--key', default='F:\\MixerWorkspace\\honeycomb\\__signfiles\\ngame.pk8',
              help='包含签名者私钥的文件的名称。该文件必须使用 PKCS #8 DER 格式。')
@click.option('-cert', '--cert', default='F:\\MixerWorkspace\\honeycomb\\__signfiles\\ngame.x509.pem',
              help='包含签名者证书链的文件的名称。此文件必须使用 X.509 PEM 或 DER 格式。')
@click.option('-a', '--align', type=click.BOOL, default=True, help='签名后执行对齐命令')
def sign(ctx, keystore, ks_pass, key_alias, key_pass, key, cert, align):
    src = ctx.obj['src']
    out = ctx.obj['out']

    # 签名之前先执行对齐
    if align:
        align_out_path = src.replace('.apk', '_aligned.apk')
        cmd = 'zipalign -p -f 4 "{}" "{}"'.format(src, align_out_path)
        os.system(cmd)

        os.remove(src)
        os.rename(align_out_path, src)
    
    cmd = ''
    if keystore is not None and ks_pass is not None and key_alias is not None:
        # 使用包含公钥和私钥的密钥库文件进行签名
        cmd = 'apksigner sign --ks {} --ks-pass pass:{} --ks-key-alias {}'.format(keystore, ks_pass, key_alias)
        if key_pass is not None:
            cmd += ' --key-pass pass:{}'.format(key_pass)
        if out is not None:
            cmd += ' --out {}'.format(out)
        cmd += ' ' + src
    elif key is not None and cert is not None:
        # 使用公钥和私钥文件进行签名
        cmd = 'apksigner sign --key {} --cert {}'.format(key, cert)
        if out is not None:
            cmd += ' --out {}'.format(out)
        cmd += ' ' + src
    else:
        print("参数输入错误，请使用--help命令查看命令帮助文档")
    os.system(cmd)
    

if __name__ == '__main__':
    apkmaker()
