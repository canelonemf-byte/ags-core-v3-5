import os, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
os.environ['AGS_API_KEY'] = 'test-key'
os.environ['LITELLM_MASTER_KEY'] = 'test-key'
os.environ['LITELLM_BASE_URL'] = 'http://127.0.0.1:9'  # sin LLM real en tests
os.environ.setdefault('AGSGPT_DATA_DIR', tempfile.mkdtemp(prefix='agsgpt-test-'))
os.environ.pop('AGSGPT_CKPT_DIR', None)
os.environ.setdefault('AGS_REPORTS_DIR', tempfile.mkdtemp(prefix='agsgpt-reports-'))
