---
type: reference
aliases:
  - Reason Network 검토
description: Source-based review of Reason Network pricing, installation changes, messaging boundaries, and a small optional pilot for a minimal agent system.
author:
  - Codex
date created: 2026-10-28
date modified: 2026-10-28
tags:
  - ai-agent
  - reason-network
  - cost
status: reviewed-not-installed
collectionPurpose: 최소한의 에이전트 시스템에서 기기와 에이전트 간 통신의 비용·적용 조건을 판단하기 위한 참고자료
mainVaultRelated: []
mainVaultCmds: ""
source:
  - https://reasonmachines.com/network
  - https://docs.reasonmachines.com/docs/network
  - https://github.com/reason-machines/reason-network/tree/29a96dc22dc0fd8904ef71f8487355135bdfb6f8
---

# Reason Network 비용·적용 검토

확인일: 2026-10-28. 공식 웹 문서와 엔진 커밋 `29a96dc22dc0fd8904ef71f8487355135bdfb6f8`을 확인했다. 이 문서는 원문 사본이 아닌 검토 요약이다. **실제 설치·계정 생성·가입·데몬 및 설정 변경은 하지 않았다.**

## 비용과 계정

- 현재 Reason Network는 카드·유료 플랜 없이 무료이며, 설정용 Reason CLI도 무료다. CLI는 비공개 소프트웨어이고, 통신 엔진은 `MIT OR Apache-2.0`이다. Cloud Reason 세션의 기존 요금은 별도로 발생한다. [공식 소개·비용 FAQ](https://reasonmachines.com/network), [엔진 라이선스](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/README.md#license)
	- Claude·Codex 등 기존 모델의 구독·API 사용료가 무료로 바뀌는 것은 아니다. 운영비 산정에는 추가 추론·반복 호출, 장비 전력·인터넷, 선택한 VPS·자체 릴레이 비용을 더한다. 이는 적용 시 계산할 비용 항목이다.
- 공식 시작 절차는 Reason 로그인으로 계정을 만들거나 기존 계정을 사용하고, 다른 컴퓨터에서도 같은 계정으로 연결한다. 이름 검증도 이 로그인에 연결된다. [공식 시작 안내](https://docs.reasonmachines.com/docs/network#get-started)
	- 독립 오픈소스 엔진은 릴리스에서 받아 로그인 없이 `init`·`join`할 수 있으나 이름은 미인증이다. 무료 로그인 경로와 계정 없는 엔진 경로를 구분한다. [고정 커밋의 배포 설계](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/DESIGN.md#install-ux-m3)
- 사용자 인용의 “맥북·맥 스튜디오에서 50개 세션” 사례는 이번 조사에서 실행 조건·실사용 비용·성능을 독립 검증하지 못했다. 설계의 약 50대 컴퓨터 규모 문구는 별개이며, 50개 에이전트의 동시 추론 성능·요금 보장이 아니다. 공개 자료에서 확정 SLA·무료 용량 상한·장기 가격 보장은 확인하지 못했다. [네트워크 설계](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/DESIGN.md#network-layer-m1)

## 최소 구성에서의 역할

- **선택형 에이전트 간 통신 연결**로 검토한다. 기존 메신저·Paseo·CLI로 사용자 접속을 해결한 뒤, 서로 다른 실행 세션이 직접 질의·응답해야 할 때 추가한다. 이는 이 패키지의 설계 제안이다. [백엔드 설계](<../10_구축/백엔드·기기 연속성·비용 설계.md>)
- 컴퓨터마다 데몬을 두고 팀의 세션 목록·작업 상태를 발견하여 메시지를 전달한다. 각자의 대화 이력·메모리·파일·작업 실행 상태를 자동으로 하나로 합치는 기능으로 해석하지 않는다. 대화를 다른 실행 컴퓨터로 옮기면 네트워크에서 별도 세션으로 식별한다. 휴대폰으로 같은 호스트의 대화에 원격 접속하는 경우와 구분한다. [엔진 README](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/README.md), [세션 설계](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/DESIGN.md#addresses)
	- 메모리·위키의 정본과 작업 인계 규칙은 기존 설계를 유지한다. 메시지에는 업무 ID·요청 범위·결과 위치를 넣고, 필요한 내용만 정본에 반영하는 방식을 제안한다.
- `serve`는 요청을 처리할 헤드리스 작업자를 여는 별도 기능이다. 열린 대화 연결과 구분하며, 엔진 연결 자체가 모든 컴퓨터의 작업을 대신 실행하지는 않는다. [공식 작업자 안내](https://docs.reasonmachines.com/docs/network#put-an-agent-to-work-for-the-team)
	- Hermes 전용 통합은 해당 커밋에서 아직 릴리스되지 않은 동반 세션 API를 요구한다고 명시한다. 제품 이름만으로 즉시 연동 가능하다고 판단하지 않고 설치 버전·전달 방식을 확인한다. [에이전트별 전달 설계](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/DESIGN.md#getting-messages-into-agents)

## 켜짐·꺼짐과 전달 상태

| 상태 | 가능한 일과 한계 |
| --- | --- |
| 양쪽 컴퓨터·데몬과 수신 실행기가 사용 가능 | 세션 메시지 전달 후 해당 실행기가 처리한다. 즉시 깨우기·다음 도구 호출·폴링 등 전달 방식은 에이전트별로 다르다. |
| 수신 컴퓨터가 꺼짐 | 송신 측 outbox가 재전송을 기다린다. 수신 측 접수·모델 실행 완료로 표시하지 않는다. |
| 컴퓨터는 켜졌으나 대상 대화가 오프라인 | 대화 식별·보존 조건에 따라 기다린다. 일반 세션은 마지막 확인 약 하루 후 잊히며 미독 메시지도 삭제될 수 있다. 영구 terminal/listen 메일함은 예외다. |
| 모든 사용자 컴퓨터가 꺼짐 | 로컬 작업은 실행되지 않는다. 호스티드 봇도 사용자 컴퓨터를 경유하므로 이를 독립 상시 서버로 간주하지 않는다. |

전달·읽음·처리 완료를 구분한다. 오프라인 컴퓨터 대신 메일과 팀 이력을 맡는 상시 anchor는 해당 커밋의 향후 M4 항목이다. 자동 장애 전환이나 무기한 보관을 전제하지 않는다. [전달·보관 설계](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/DESIGN.md#network-layer-m1), [호스티드 연결](https://docs.reasonmachines.com/docs/network#hosted-assistants-grok-bot-muse-chatgpt)

## 설치 변경과 보안 경계

- 설정 과정은 탐지한 에이전트의 MCP·hooks·skill/플러그인과 사용자 설정을 수정하고, 로그인 시 실행되는 데몬 서비스를 구성할 수 있다. 기존 설정에는 `.bak-reason` 최초 백업 로직이 있으나 도입 전 별도 사본·차이를 남기는 편이 좋다. [공식 설정 안내](https://docs.reasonmachines.com/docs/network#get-started), [설정 코드](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/src/setup.rs)
	- 이 커밋은 Codex `config.toml`의 Reason Network MCP 항목에 `default_tools_approval_mode = "approve"`를 넣고 `hooks.json`을 작성한다. Claude 설정에는 `mcp__reason-network__ask_user` 허용을 추가한다. 이를 모든 도구·셸의 무제한 실행 허가로 해석하지 않는다. [설정 코드](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/src/setup.rs)
- 기본값은 `inbound=accept`, 폴더 제외 없음, `share_paths=false`, `share_unmanaged=false`, `auto_update=true`다. 전체 경로를 숨겨도 저장소·브랜치 등 세션 정보는 공유될 수 있다. [기본값 코드](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/src/config.rs), [공유 정보](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/README.md#how-it-works)
	- `hold`·승인·거절은 **다른 컴퓨터에서 들어오는 메시지**에 적용된다. 같은 컴퓨터의 세션 간 메시지는 이 정책을 거치지 않는다. 메시지 수락은 요청된 작업 전체의 권한 부여와 별개다. [신뢰 설계](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/DESIGN.md#trust-and-safety)
	- 폴더 `off`는 세션 등록·전송을 제한하며 `on`은 제외를 해제한다. 다중 세션 공유 MCP에서 hooks가 실행되지 않으면 MCP 프로세스 폴더로 판단하는 한계가 있다. OS·실행기 권한과 데이터 반출 정책을 대체하지 않는다. [폴더 기본값·한계](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/DESIGN.md#config)
- 컴퓨터 간 통신은 E2E 암호화되고 기본 릴레이는 Reason, 주소 조회는 n0를 사용한다. 자체 릴레이를 지정하면 해당 피어 연결에 기본 Reason 릴레이·n0를 사용하지 않는다. 로그인·호스티드 서비스까지 사라진다는 뜻은 아니다. [연결 설명](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/README.md#how-it-works)
	- 호스티드 봇은 Reason 서버를 통한다. 로컬 피어 간 E2E 설명을 호스티드 요청의 서버 비열람 보장으로 확대하지 않는다. 조직 자료는 서비스·데이터 범위별 기존 반출 정책으로 판단한다. [공식 보안 설명](https://reasonmachines.com/network#security), [패키지 보안 운영](<../10_구축/접속 경계와 보안 운영.md>)
- 팀원에게 초대·제거 권한이 있고 제거된 기기의 암호학적 권한 소멸에도 설계상 한계가 있다. 기업용 세분화 권한·강제 회수 체계가 갖춰졌다고 전제하지 않는다. [멤버십 설계](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/DESIGN.md#network-layer-m1)

## 무료로 시작하는 작은 시험 제안

아래는 자체 설계한 도입 순서이며 현재 수행한 작업이 아니다. 읽기·문서 갱신마다 별도 승인을 요구하지 않고, 정해진 연결·실행·반출 권한을 따른다.

1. 본인 컴퓨터 두 대와 민감정보 없는 1–2개 세션을 고른다. 기존 모델 요금·사용량 한도를 적고, 시험용 OS 계정/프로필 등으로 연결 범위를 좁힌다.
2. 설치할 버전과 설정 변경 목록을 기록하고 원래 MCP·hooks·권한·로그인 서비스 설정을 백업한다. 자동 업데이트를 사용할지도 정한다.
3. 연결 후 실제 공개 세션·폴더 제외를 확인한다. 외부 기기 메시지는 시험 중 `hold`로 두고, 같은 기기 예외와 실행기 권한을 함께 시험한다.
4. 작은 요청 한 건으로 전달·읽음·결과를 구분한다. 수신기 종료·재시작, 폴더 차단, 거절, 인계와 중복 요청 시 동작을 확인한다.
5. 모델 사용량과 작업당 비용을 비교하고 연결 제거·설정 복구를 확인한다. 필요할 때만 다른 사람·호스티드 봇·상시 작업자로 넓힌다.

시험 결과와 확정 비용은 [검증·운영 기록](<../30_양식/검증·운영 기록.md>)에 남긴다. 도입 여부·컴퓨터·에이전트 버전·허용 폴더·보존 요구·월 예산·조직 허용 범위는 아직 미정이다.

## 능동 운영·최종 인계에서 다시 확인할 부분

2026-10-28 재확인한 공식 main도 위 고정 커밋 `29a96dc22dc0fd8904ef71f8487355135bdfb6f8`과 같았다. 기존 비용·수신 정책·설정 변경·OFF 조건을 유지하며, [선택 구성 검토·최종 체크리스트](<../10_구축/선택 구성 검토·최종 체크리스트.md>)를 통해 도입/미도입/보류와 실제 시험 상태를 최종 구축 보고서에 명시한다.

- 메시지 전달과 실행기를 깨우는 방법은 하네스마다 다르다. push/idle wake, 다음 도구 호출·턴, inbox 조회 등을 해당 어댑터·버전에서 확인한다. 같은 네트워크에 있다는 사실만으로 모든 실행기가 사용자 입력 없이 즉시 작업한다고 보장하지 않는다. [전달 계층 설계](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/DESIGN.md#getting-messages-into-agents)
- Hermes native plugin은 해당 문서의 미출시 companion session API 조건이 있다. 구버전의 일반 MCP 경로와 실제 wake 권한/설정을 구분한다. OmO·OpenClaw도 이름만으로 native 자동 연결 지원을 확정하지 않는다. [Hermes 통합 조건](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/integrations/hermes/README.md)
- `wake_me`·호스티드 봇의 웹훅/폴링은 상대 플랫폼의 기동 경로를 연결하는 방식이다. 공통 업무 일정·완료 근거·taskId·담당·권한을 유지하는 [능동 운영](<../10_구축/능동 운영과 완료 추적.md>)을 별도로 구성·시험한다. [호스티드 연결](https://reasonmachines.com/network)
- 작은 텍스트 파일 전달은 이 커밋 기준 최대 10개·개별 256KB·합계 512KB이며 수신 사본을 자동으로 열거나 실행하지 않는다. 파일 동기화나 위키 정본 공유와 구분한다. 실제 전송할 때 내용·대상·자료 반출 권한을 확인한다. [공식 파일 전달 안내](https://github.com/reason-machines/reason-network/blob/29a96dc22dc0fd8904ef71f8487355135bdfb6f8/README.md)

이번 확인은 공식 문서·소스 대조이며 Reason 설치·계정 연결·데몬 변경·실제 메시지/파일 전송·업무 실행은 수행하지 않았다.
