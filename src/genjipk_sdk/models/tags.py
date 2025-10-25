from typing import Literal

import msgspec


class TagsSearchFilters(msgspec.Struct, omit_defaults=True):
    guild_id: int
    # filters
    name: str | None = None  # raw name
    fuzzy: bool = False  # fuzzy (pg_trgm)
    include_aliases: bool = True
    only_aliases: bool = False
    owner_id: int | None = None
    # special modes
    random: bool = False  # random tag
    by_id: int | None = None  # lookup by tag_id
    # output controls
    include_content: bool = False  # return content
    include_rank: bool = False
    # sorting & paging
    sort_by: Literal["name", "uses", "created_at"] = "name"
    sort_dir: Literal["asc", "desc"] = "asc"
    limit: int = 20
    offset: int = 0


class TagRowDTO(msgspec.Struct, omit_defaults=True):
    id: int
    guild_id: int
    name: str
    owner_id: int
    is_alias: bool = False
    canonical_name: str | None = None
    uses: int | None = None
    content: str | None = None
    rank: int | None = None


class TagsSearchResponse(msgspec.Struct):
    items: list[TagRowDTO]
    total: int | None = None  # optionally returned for paging UIs
    suggestions: list[str] | None = None  # for fuzzy fallbacks


class OpBase(msgspec.Struct):
    op: str


class OpCreate(OpBase):
    op: Literal["create"]
    guild_id: int
    name: str
    content: str
    owner_id: int


class OpAlias(OpBase):
    op: Literal["alias"]
    guild_id: int
    new_name: str
    old_name: str
    owner_id: int


class OpEdit(OpBase):
    op: Literal["edit"]
    guild_id: int
    name: str
    new_content: str
    owner_id: int


class OpRemove(OpBase):
    op: Literal["remove"]
    guild_id: int
    name: str
    requester_id: int


class OpRemoveById(OpBase):
    op: Literal["remove_by_id"]
    guild_id: int
    tag_id: int
    requester_id: int


class OpClaim(OpBase):
    op: Literal["claim"]
    guild_id: int
    name: str
    requester_id: int


class OpTransfer(OpBase):
    op: Literal["transfer"]
    guild_id: int
    name: str
    new_owner_id: int
    requester_id: int


class OpPurge(OpBase):
    op: Literal["purge"]
    guild_id: int
    owner_id: int
    requester_id: int


class OpIncrementUsage(OpBase):
    op: Literal["increment_usage"]
    guild_id: int
    name: str


TagOp = OpCreate | OpAlias | OpEdit | OpRemove | OpRemoveById | OpClaim | OpTransfer | OpPurge | OpIncrementUsage


class TagsMutateRequest(msgspec.Struct):
    ops: list[TagOp]  # supports batching in one HTTP call


class TagsMutateResult(msgspec.Struct, omit_defaults=True):
    ok: bool
    message: str | None = None
    affected: int | None = None
    tag_id: int | None = None


class TagsMutateResponse(msgspec.Struct):
    results: list[TagsMutateResult]


class TagsAutocompleteRequest(msgspec.Struct):
    guild_id: int
    q: str
    mode: Literal["aliased", "non_aliased", "owned_aliased", "owned_non_aliased"] = "aliased"
    owner_id: int | None = None
    limit: int = 12


class TagsAutocompleteResponse(msgspec.Struct):
    items: list[str]
