# MH 와일즈 도감

몬스터 헌터 와일즈의 몬스터·무기·방어구·스킬·장식주·호석·아이템을 한국어로 찾아보는 비공식 팬 도감입니다.

**바로 보기:** https://comrade920.github.io/mhwilds-dex/

- 초성(ㄹㅇㄹㅇㅅ)·영문(rathalos)·별명(자화룡) 검색
- 몬스터 약점, 부위별 육질, 하위/상위 보상, 전용 소재 장비
- 무기 예리도·파생, 방어구 부위별 스킬, 아이템 얻는 곳·쓰이는 곳
- 휴대폰에서 "홈 화면에 추가"하면 앱처럼 열립니다

## 데이터 갱신

게임 데이터는 [mhdb-wilds-data](https://github.com/LartTyler/mhdb-wilds-data)에서 가져옵니다(현재 2026-04-14 추출본).

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/LartTyler/mhdb-wilds-data
(cd mhdb-wilds-data && git sparse-checkout set output/merged)
python3 tools/build_data.py mhdb-wilds-data/output/merged   # tools/data.json 생성
python3 tools/build.py                                     # index.html 생성
```

화면 코드는 `tools/template.html`, 데이터 가공은 `tools/build_data.py`에 있습니다.

---

비공식 팬 사이트이며 CAPCOM과 관련이 없습니다. Monster Hunter Wilds의 게임 텍스트 저작권은 CAPCOM에 있습니다.
© 2026 comrade920 · 사이트 코드, 디자인, 직접 작성한 내용은 허락 없이 복제·재배포할 수 없습니다.
