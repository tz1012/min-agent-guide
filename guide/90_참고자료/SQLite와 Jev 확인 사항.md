---
type: reference
aliases:
  - 최소 에이전트 저장소와 판단 모델 참고
description: Dated official-source findings on SQLite storage and recovery and Jev decision models, with costs, data handling, limitations, and adoption criteria.
author:
  - Codex
date created: 2026-10-28
date modified: 2026-10-28
status: documentation-verified-not-runtime-tested
tags:
  - ai-agent
  - build-package
  - storage
collectionPurpose: "폴더 안의 자료만으로 최소 에이전트 시스템의 저장소·기기 연속성·선택적 판단 모델을 설계하고, 실제 구축에서 확정할 조건을 구분한다."
mainVaultRelated: []
mainVaultCmds: ""
source:
  - https://www.sqlite.org/whentouse.html
  - https://www.sqlite.org/wal.html
  - https://www.sqlite.org/backup.html
  - https://www.postgresql.org/docs/current/high-availability.html
  - https://docs.typesafe.ai/introduction
  - https://docs.typesafe.ai/models
  - https://docs.typesafe.ai/confidence
  - https://docs.typesafe.ai/api/errors
  - https://help.typesafe.ai/articles/5974925716-how-is-submitted-data-used-or-retained
  - https://help.typesafe.ai/articles/9520184411-do-you-offer-zdr
  - https://typesafe.ai/legal/privacy-policy
---

# SQLite와 Jev 확인 사항

**확인일: 2026-10-28.** 공개 공식 문서의 핵심을 이 파일에 포함했다. 외부 링크는 근거·변경 확인용이며 패키지의 설계 검토를 시작하기 위한 필수 열람 순서가 아니다. 실제 설치·계정 연결·성능·복구 시험은 수행하지 않았다. 적용안은 [백엔드·기기 연속성·비용 설계](<../10_구축/백엔드·기기 연속성·비용 설계.md>), 선택값은 [구축 결정·규칙 기록](<../30_양식/구축 결정·규칙 기록.md>)에 남긴다.

## 역할 구분

- SQLite는 작업·승인·중복·실행 상태와 기억 메타데이터를 저장하는 DB다. LLM Wiki는 원문·지식·판단 근거·절차를 사람이 검토할 수 있게 관리한다.
- 이 문서의 JEV는 TypeSafe의 Jev로 해석한다. Jev는 상태와 질문을 받아 구조화된 판단을 반환하는 모델이며, DB·위키·에이전트 실행기를 대체하지 않는다. [공식 소개](https://docs.typesafe.ai/introduction)

## SQLite 선택·운영 조건

| 확인한 특성 | 설계에 적용할 기준 |
| --- | --- |
| 로컬 파일 DB | 허브 한 대에 DB를 두고 다른 기기는 API로 접근하는 구성이 가능하다. 사용자 수만으로 서버 DB 전환을 결정하지 않는다. |
| 동시 쓰기 | DB 파일별 쓰기는 한 번에 하나다. 짧은 쓰기를 대기시킬 수 있으면 사용 가능하다. 모델·외부 API 응답을 기다리는 동안 DB 쓰기 트랜잭션을 열어 두지 않는다. |
| WAL | 읽기와 쓰기를 병행할 수 있으나 같은 호스트를 전제로 하며 네트워크 파일시스템에서 동작하지 않는다. 실행 중 DB를 기기 간 동기화해 공동 사용하지 않는다. |
| 상태와 내구성 | WAL도 영속 상태의 일부다. 실행 중 `.db`만 복사하거나 WAL을 임의 삭제하지 않는다. 동기화 설정에 따른 전원 장애 시 데이터 손실 허용 범위를 정한다. |
| 백업 | Online Backup API 또는 `VACUUM INTO` 등으로 일관된 사본을 만든 뒤 전송한다. 백업 생성 성공과 실제 복원 성공을 따로 확인한다. |

근거: [SQLite 적용 범위](https://www.sqlite.org/whentouse.html), [WAL 동작·주의사항](https://www.sqlite.org/wal.html), [온라인 백업](https://www.sqlite.org/backup.html).

- 설치 기록에는 실제 앱이 링크한 SQLite 버전, DB 경로·파일 권한, journal·synchronous 설정, busy 처리·checkpoint 정책, 디스크 여유, 백업 위치·주기·보존·복구 증거를 남긴다.
	- 확인한 공식 문서는 WAL-reset 수정이 3.51.3 이상 또는 백포트 3.44.6·3.50.7에 포함됐다고 명시한다. 배포 시 수정 포함 여부를 확인한다.
- PostgreSQL 등 서버 DB 전환은 다수 동시 쓰기를 대기시킬 수 없거나, 여러 실행 서버의 공유 DB·복제·고가용성이 실제 요구일 때 검토한다. 처리량·쓰기 대기·실패율·복구 시간·허용 손실로 판단한다.
	- 서버 DB로 바꿔도 고가용성은 자동 완성되지 않는다. 복제·장애 전환·접근 통제·백업 구성을 선택하고 시험한다. [PostgreSQL 동시성](https://www.postgresql.org/docs/current/mvcc.html), [고가용성·복제](https://www.postgresql.org/docs/current/high-availability.html)

## Jev 제품·비용·실패 처리

| 항목 | 확인한 내용과 적용 기준 |
| --- | --- |
| 현재 버전·단가 | 공식 모델 문서 기준 `jev-1.14.0`은 2026-10-14 공개. 입력 100만 토큰당 USD $0.042, 출력 무료다. 생성 모델·저장소·네트워크·재시도 비용은 별도다. |
| 기본 한도 | 요청 전체 64k, 개별 질문 32k 토큰. 조직별 초당 토큰·요청 한도는 계정 콘솔값이며 여기서 확인하지 않았다. |
| 긴 문맥 | 별도 헤더로 요청·질문 한도를 각각 262k로 높이는 옵션이 있다. 공식 문서도 기본 한도 대비 지연·정확도 손실을 명시한다. 기본 필수 설정으로 삼지 않는다. |
| 버전 변경 | `jev-latest` 별칭의 대상은 바뀔 수 있다. 질문·임계값을 검증했다면 버전 ID를 고정하고 실제 응답의 모델 버전을 기록한다. |
| confidence | Choice·Score는 확률분포를 요약한 confidence를 제공한다. Noul은 확률만 반환한다. 수치를 정확성 보장·업무 권한으로 해석하지 않는다. |
| 실패·대체 | 429·529는 지수 백오프 재시도 대상이다. 총시간·횟수·비용 상한과 기존 모델·코드·사람으로 넘기는 조건을 정한다. |

근거: [모델·가격·한도](https://docs.typesafe.ai/models), [confidence 의미](https://docs.typesafe.ai/confidence), [요청 규칙·오류](https://docs.typesafe.ai/api/errors).

- 영어가 주된 학습 언어이므로 실제 한국어 업무 표본으로 품질·오판 비용·전체 시간·총비용을 비교한다. 작은 업무량에서는 연결 하나를 더 운영하는 비용이 절약보다 클 수 있다.
- 계산·날짜 비교·권한 집행은 코드로 처리하고 Jev에는 좁은 의미 판단을 맡긴다. [1.13 한계 문서](https://docs.typesafe.ai/model-jaggedness/jev-1.13)는 숫자·간접 추론·무관한 긴 문맥·악의적 입력의 약점을 명시하지만, 그 결과를 1.14의 검증 결과로 대체하지 않는다.

### 실제 연결·무료 범위의 추가 확인

2026-10-28 공식 도움말을 재확인했다. 이 제품은 계정/API 키와 HTTP 또는 SDK로 연결하는 판단 API다. 코딩 에이전트의 기본 생성 모델을 Jev로 교체하거나 로컬 DB처럼 설치하는 경로로 안내하지 않는다. 통합 스킬은 API를 쓰는 코드를 작성하도록 돕는 선택 도구다. [공식 시작](https://docs.typesafe.ai/introduction/quickstart), [코딩 에이전트 안내](https://docs.typesafe.ai/introduction/coding-agents)

상시 무료 입력 할당량·무료 크레딧 보장은 확인하지 못했다. 출력 무료를 API 전체 무료로 해석하지 않는다. 공식 도움말은 크레딧 구매와 선택적 자동충전, 잔액 부족 시 402를 안내한다. 자동충전은 사용자가 정한 비용 정책에 따라 별도로 결정하고, 402에서 무제한 재시도하지 않으며 기존 모델/코드/사람 경로로 전환하거나 대기한다. [크레딧 관리](https://help.typesafe.ai/articles/7771619341-how-do-i-add-credits), [잔액 부족 처리](https://help.typesafe.ai/articles/5505198974-what-s-a-402-error-and-how-can-i-add-more-credits)

필수 검토·선택적 연결과 최종 보고는 [선택 구성 검토·최종 체크리스트](<../10_구축/선택 구성 검토·최종 체크리스트.md>)를 따른다. 계정 생성·키 발급·유료 호출·품질 시험은 이번 문서 작업에서 수행하지 않았다.

## 데이터 처리·미확인 범위

- 요청·응답은 모델 학습에 사용하지 않는다고 명시한다. 서비스 제공·과금·오남용 방지·telemetry 처리는 있으며, 일반 고객의 고정 보존 일수는 공개 자료에서 확인하지 못했다. [데이터 처리 안내](https://help.typesafe.ai/articles/5974925716-how-is-submitted-data-used-or-retained)
- ZDR은 엔터프라이즈 요청형이며 활성화 후에도 운영 telemetry는 남는다. 기본 활성화로 가정하지 않는다. [ZDR 안내](https://help.typesafe.ai/articles/9520184411-do-you-offer-zdr)
- 개인정보 정책은 미국 저장·처리를 명시한다. 자체 VPC·온프레미스 지원은 공개 FAQ의 질문만 확인돼 지원 여부를 확정하지 못했다. [개인정보 정책](https://typesafe.ai/legal/privacy-policy), [기업용 페이지](https://typesafe.ai/enterprise)
- Jev-Mem은 별도의 [연구 논문](https://arxiv.org/abs/2609.23986)·[저자 구현](https://github.com/libingzheren/Jev-Mem)이 있다. [독립 jevmem 구현](https://github.com/illescasDaniel/jev-mem)은 저자·TypeSafe와 무관하다고 명시한다. 이를 공식 Jev 제품이나 검증된 운영 메모리로 혼동하지 않는다.
- 이 자료만으로 계정의 이용 가능 여부·계약 적합성·실제 품질을 확정하지 않는다. 선택한 기능만 적용하고, 외부 판단 호출을 꺼도 대표 업무를 수행할 대체 경로를 유지한다.
