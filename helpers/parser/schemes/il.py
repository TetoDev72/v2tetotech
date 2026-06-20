from dataclasses import dataclass, field, asdict
@dataclass
class ILNode:
    protocol: str = ""; name: str = ""; server: str = ""; port: int = 443
    uuid: str = ""; flow: str = ""; network: str = "tcp"; security: str = "tls"
    sni: str = ""; fp: str = "chrome"; pbk: str = ""; sid: str = ""
    alpn: list = field(default_factory=list); path: str = ""; host: str = ""
    method: str = ""; extra: dict = field(default_factory=dict)
    def to_dict(self): return {k: v for k, v in asdict(self).items() if v not in (None, "", [], {})}

@dataclass
class ILSubscription:
    nodes: list = field(default_factory=list)
    meta: dict = field(default_factory=dict)
