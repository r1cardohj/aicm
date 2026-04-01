from pathlib import Path
from typing import Callable
from collections import namedtuple

import sys
import os
import argparse

from llama_cpp import Llama
import requests

ModelInfo = namedtuple('ModelInfo', ['req_id', 'filename', 'prompt_fmt'])
SKIP_PREFIXES = ('#', '"', "'", 'This', 'The ', 'Here ', 'Note: ')

INSTALL_ENDPOINT = os.environ.get('INSTALL_ENDPOINT', 'https://huggingface.co')

## MODEL STUFF

models_map = {
    'qwen2.5': ModelInfo(
        req_id='bartowski/Qwen2.5.1-Coder-1.5B-Instruct-GGUF',
        filename='Qwen2.5.1-Coder-1.5B-Instruct-Q4_K_M.gguf',
        prompt_fmt='<|fim_prefix|>{prefix}<|fim_suffix|>{suffix}<|fim_middle|>',
    ),
    'qwen2.5-lite': ModelInfo(
        req_id='bartowski/Qwen2.5-Coder-0.5B-Instruct-GGUF',
        filename='Qwen2.5-Coder-0.5B-Instruct-Q4_K_M.gguf',
        prompt_fmt='<|fim_prefix|>{prefix}<|fim_suffix|>{suffix}<|fim_middle|>',
    ),
}


_AICM_DIR = Path.home() / Path('.aicm')


def hf_url(req_id, file_name):
    """get huggingface url for downloading model files"""
    return f'{INSTALL_ENDPOINT}/{req_id}/resolve/main/{file_name}'


def get_dir():
    if not _AICM_DIR.exists():
        _AICM_DIR.mkdir()
    return _AICM_DIR


def get_models_dir():
    get_dir()  # Ensure base directory exists

    models_dir = _AICM_DIR / 'models'
    if not models_dir.exists():
        models_dir.mkdir()
    return models_dir


def download_file(
    url: str,
    save_path: Path | str,
    chunk_size: int = 8192,
    headers: dict[str, str] | None = None,
    progress_callback: Callable[[int, int], None] | None = None,
    resume: bool = True,
) -> str:
    if isinstance(save_path, str):
        save_path = Path(save_path)

    save_path.parent.mkdir(parents=True, exist_ok=True)
    downloaded = save_path.stat().st_size if resume and save_path.exists() else 0

    req_headers = headers.copy() if headers else {}

    if downloaded > 0:
        req_headers['Range'] = f'bytes={downloaded}'
        print(f'Resuming download from byte {downloaded}...')

    resp = requests.get(url, headers=req_headers, stream=True)
    resp.raise_for_status()

    total_size = int(resp.headers.get('Content-Length', 0))
    if 'content-range' in set(key.lower() for key in resp.headers):
        total_size += downloaded

    mode = 'ab' if downloaded > 0 else 'wb'

    with open(save_path, mode) as f:
        for chunk in resp.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if progress_callback:
                    progress_callback(downloaded, total_size)

            if total_size > 0 and downloaded >= total_size:
                break

    return str(save_path)


def print_progress(current: int, total: int):
    if total > 0:
        percent = (current / total) * 100
        print(
            f'Downloaded {current} of {total} bytes ({percent:.2f}%)',
            end='\r',
            flush=True,
        )
    else:
        print('Downloaded {current} bytes', end='\r', flush=True)


def install_model(alias: str):
    if alias not in models_map:
        raise ValueError(f"Model alias '{alias}' not found in models_map")

    model_info = models_map[alias]
    url = hf_url(model_info.req_id, model_info.filename)
    save_path = get_models_dir() / model_info.filename

    print(f"Downloading model '{alias}' from {url}...")
    download_file(url, save_path, progress_callback=print_progress)
    print(f"\nModel '{alias}' downloaded to {save_path}")


class CodeComplteModel:
    def __init__(self, llm: Llama, model_info: ModelInfo):
        self.llm = llm
        self.model_info = model_info

    def complete(self, prefix, suffix: str = '', max_tokens: int = 512) -> str:
        if suffix:
            prompt = self.model_info.prompt_fmt.format(prefix=prefix, suffix=suffix)
        else:
            prompt = self.model_info.prompt_fmt.format(prefix=prefix, suffix='')

        output = self.llm(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.1,  # low temperature for more deterministic output
            top_p=0.95,
            stop=[
                '<|fim_prefix|>',
                '<|fim_suffix|>',
                '<|fim_middle|>',
                '<|endoftext|>',
                '\n\n#',  # 停止：空行+注释（解释开始）
                '\n\n"',  # 停止：空行+引号（文档字符串）
                '\n\nHere',  # 停止：解释性文字
                '\n\nThis',  # 停止：解释性文字
                '\n\nThe',  # 停止：解释性文字
                '\n\n##',  # 停止：markdown标题
                '```',  # 停止：代码块结束
            ],
            echo=False,
        )

        return output['choices'][0]['text']

    def complete_line(
        self, prefix: str, suffix: str = '', max_tokens: int = 32
    ) -> str:
        prompt = self.model_info.prompt_fmt.format(prefix=prefix, suffix=suffix)
        output = self.llm(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.1,
            top_p=0.95,
            stop=[
                '<|fim_prefix|>',
                '<|fim_suffix|>',
                '<|fim_middle|>',
                '<|endoftext|>',
                '\n',  # 关键：遇到换行符立即停止
                '\r',
            ],
            echo=False,
        )
        return output['choices'][0]['text']

    def insert_code(self, prefix: str, suffix: str, max_tokens: int = 64) -> str:
        prompt = self.model_info.prompt_fmt.format(prefix=prefix, suffix=suffix)
        output = self.llm(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.1,
            top_p=0.95,
            stop=[
                '<|fim_prefix|>',
                '<|fim_suffix|>',
                '<|fim_middle|>',
                '<|endoftext|>',
                '\n\n',
                '\n#',
                '\n//'
            ],
            echo=False,
        )
        return output['choices'][0]['text']


def load_cmp_model(alias: str) -> CodeComplteModel:
    if alias not in models_map:
        raise ValueError(f"Model alias '{alias}' not found in models_map")

    model_path = get_models_dir() / models_map[alias].filename

    llm = Llama(
        model_path=str(model_path),
        n_ctx=32768,
        n_gpu_layers=-1,
        n_batch=512,
        verbose=False,
        chat_format='chatml',
    )

    return CodeComplteModel(llm, models_map[alias])


def high_light_print(text):
    print('\033[1;32m' + text + '\033[0m')  # green


def main():
    parser = argparse.ArgumentParser(description='aicm: AI Complete Me')
    parser.add_argument(
        '--install',
        nargs='?',
        const='qwen2.5-lite',
        metavar='MODEL',
        help='Install the model (default: qwen2.5-lite, options: qwen2.5, qwen2.5-lite)',
    )
    parser.add_argument(
        '-m',
        '--model',
        default='qwen2.5-lite',
        metavar='MODEL',
        help='Model to use for completion (default: qwen2.5-lite, options: qwen2.5, qwen2.5-lite)',
    )
    parser.add_argument(
        '-l', '--line', help='complete current line', action='store_true'
    )
    parser.add_argument(
        '-s',
        '--suffix',
        default='',
        metavar='SUFFIX',
        help='suffix text for fill-in-the-middle completion',
    )
    args = parser.parse_args()

    if args.install:
        install_model(args.install)
        return

    if args.model not in models_map:
        print(
            f"Error: Unknown model '{args.model}'. Available: {', '.join(models_map.keys())}",
            file=sys.stderr,
        )
        sys.exit(1)

    if not sys.stdin.isatty():
        text = sys.stdin.read().rstrip('\n')
        model = load_cmp_model(args.model)
        res = None
        if args.line:
            res = model.complete_line(text, args.suffix, max_tokens=256)
        elif args.suffix:
            res = model.insert_code(text, args.suffix)
        else:
            res = model.complete(text, max_tokens=256)
        print(text, end='')
        high_light_print(res)
        if args.suffix:
            print(args.suffix)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
