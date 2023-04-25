import logging

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

console = logging.StreamHandler()
console.setLevel(logging.ERROR)

log.addHandler(console)