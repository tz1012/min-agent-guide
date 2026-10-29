---
type: integration-guide
aliases:
  - Google Calendar·Gmail 연결 진행
description: Agent-assisted Google account setup with existing connectors, scoped OAuth, user and administrator handoffs, host-specific verification, recovery and revocation.
author:
  - Codex
date created: 2026-10-29
date modified: 2026-10-29
tags:
  - ai-agent
  - google-workspace
  - integration
status: documentation-verified-runtime-unverified
---

# Google 계정 연결·대리 설정

**Google Calendar·Gmail을 선택하면 에이전트는 기존 연결 확인부터 설정 준비·사용자 인증 안내·실제 결과 재조회·운영 연결까지 진행한다.** 사용자가 직접 해야 하는 로그인·2단계 인증·동의와 관리자 결정을 제외하고, 허용된 설정은 사용 가능한 API·CLI·MCP·웹 화면으로 대신 수행한다. 설명만 제공하고 사용자가 모든 설정을 다시 하게 만드는 것을 기본 흐름으로 삼지 않는다.

공식 문서 확인일은 **2026-10-29**이다. 이 문서는 구축 가이드이며 실제 계정 열람·연결·설치·API 호출·초대·메일 발송을 수행한 기록이 아니다. 제품·화면·정책이 바뀌면 대상 환경에서 다시 확인한다.

[연결 대상별 설정 가이드](<연결 대상별 설정 가이드.md>)의 Google 분기를 구체화한다. 일반 메일 프로토콜·로컬 앱은 [이메일 연결과 로컬 앱](<이메일 연결과 로컬 앱.md>), Sheets+Drive DB는 [Google 도구 기반 최소 구성](<Google 도구 기반 최소 구성.md>), 일정과 할 일의 차이는 [일정·할 일 도구 확인 사항](<../90_참고자료/일정·할 일 도구 확인 사항.md>)을 필요한 경우에만 함께 읽는다.

## 1. 기존 선택과 권한부터 확인한다

이미 답한 내용은 재사용하고, 아래에서 실제 첫 업무에 필요한 미정 사항만 묻는다. 개인·기업·복수 계정을 모두 연결할 수 있지만 계정별 허용 범위를 합치지 않는다.

| 확인할 것 | 확정할 내용 |
| --- | --- |
| 사용할 실행기 | 사용자가 선택한 에이전트·제품/에디션/버전·프로필. 연결 때문에 다른 실행기로 바꾸거나 CLI를 무조건 설치하지 않음 |
| 실제 운영 위치 | 집 PC·노트북·내부 서버·승인된 클라우드, 실행 OS 사용자·서비스, 예약 담당 호스트 |
| 계정·대상 | 개인 Gmail 또는 Workspace, 연결 사용자, 사서함·calendar ID·조회 기간·대상 라벨/자료 |
| 하고 싶은 일 | 일정 조회/제안/생성/수정/삭제/초대, 메일 조회/첨부/초안/발신/읽음/라벨/휴지통을 각각 선택 |
| 실행 조건 | 요청할 때만 또는 정한 시간/새 입력에 능동 실행, 시간대·조용한 시간·한도·중단 방법 |
| 정보·행동 경계 | 개인/기업 자료, 외부 모델에 보낼 범위, 허용 수신자/참석자, 쓰기·검토 규칙 |
| 성공 기준 | 지정 표본 조회와 선택한 변경의 재조회, 재시작·회수 증거. 미선택 기능은 적용 제외 |

먼저 현재 실행기에 있는 공식·승인된 커넥터의 계정과 실제 지원 도구를 확인한다. 필요한 기능이 있으면 재사용한다. 자체 OAuth 앱·GCP 프로젝트·서버는 기존 연결로 충족하지 못할 때만 추가한다. 공용 커넥터를 쓰는 사용자에게 새 Cloud 프로젝트를 필수로 만들게 하지 않는다.

커넥터가 실제 scope·토큰 만료 정보를 노출하지 않으면 공개 권한 설명·제품 설정·허용 표본 조회로 확인 가능한 범위를 검증하고 미노출 값은 미확인으로 기록한다. 내부 토큰 추출을 요구하거나 조회 성공만으로 모든 권한·자동 갱신을 확인했다고 표시하지 않는다.

**현재 대화의 Google 연결은 OpenClaw·Hermes 등 별도 운영 호스트의 에이전트로 자동 이전되지 않는다.** 같은 Google 계정을 써도 커넥터 제공자·OAuth client·토큰 저장소·OS 사용자·도구 권한이 다를 수 있다. 운영 호스트에서 지원되는 연결 경로를 별도로 확인하고 연결 ID와 자격증명 참조를 기록한다. 기존 커넥터의 토큰을 추출해 다른 실행기로 복사하는 것을 기본안으로 삼지 않는다.

## 2. 행동과 OAuth 범위를 구분한다

OAuth scope는 Google이 허용하는 접근 범위다. 사용자가 정한 더 좁은 업무 범위는 어댑터의 대상 허용 목록·노출 도구·행동 정책에서도 집행한다. 실제 동의받은 scope가 요청한 범위와 일치하는지 확인하고, 일부만 허용되면 해당 기능만 연결한다.

### Calendar

아래 scope는 `https://www.googleapis.com/auth/` 뒤에 붙는 이름이다. 선택한 API 메서드가 받는 범위와 대상 캘린더 권한을 함께 확인한다.

| scope 예시 | 허용 범위와 선택 시 주의 |
| --- | --- |
| `calendar.readonly` | 접근 가능한 캘린더 조회·다운로드. 이벤트만 읽으면 더 좁은 `calendar.events.readonly` 검토 |
| `calendar.events` | 접근 가능한 캘린더의 이벤트 조회·편집. 공유 캘린더의 실제 쓰기 권한을 새로 주지는 않음 |
| `calendar.events.owned` | 사용자가 소유한 캘린더의 이벤트 조회·생성·수정·삭제. 에이전트가 만든 일정만 제한하는 범위가 아님 |
| `calendar.calendarlist.readonly` | 캘린더 목록 조회가 필요한 경우. events 권한만으로 목록 조회까지 된다고 가정하지 않음 |

어느 범위도 임의의 캘린더 한 개만 지정하는 허용 목록은 아니다. 알려진 calendar ID를 제한해 사용하고, 목록 선택 UI가 필요할 때만 목록 권한을 추가한다. 공유 관리 권한과 실제 캘린더 소유자는 다를 수 있으므로 공유 대상에 `events.owned`가 충분하다고 단정하지 않는다. [Calendar scope](https://developers.google.com/workspace/calendar/api/auth), [목록 조회 권한](https://developers.google.com/workspace/calendar/api/v3/reference/calendarList/list), [공유·소유권](https://developers.google.com/workspace/calendar/api/concepts/sharing)

일정 쓰기에는 시간대·종일 여부·반복의 한 회차/전체·참석자·통지 여부를 따로 정한다. **Calendar 초대는 Gmail 발신 권한 없이도 발생할 수 있다.** `sendUpdates=none`도 모든 이메일 차단을 보장하지 않으며 동기화 문제를 일으킬 수 있다. 초대를 선택하지 않았다면 참석자를 넣지 않는 허용 표본으로 시험한다. 공유 초대·참석자 알림도 외부 행동 범위에 포함한다. [이벤트 생성·sendUpdates](https://developers.google.com/workspace/calendar/api/v3/reference/events/insert)

Calendar의 일정(Event), 화면 안의 할 일(Task), 에이전트 실행 상태는 다르다. 할 일까지 원하면 Tasks 지원·scope·목록 ID를 별도 확인한다. 화면의 시간·반복·Deadline을 API에서도 모두 지원한다고 약속하지 않는다. 알림 읽음·일정 종료를 실제 업무 완료로 바꾸지 않는다. [일정·할 일 연결 계약](<../90_참고자료/일정·할 일 도구 확인 사항.md>)

### Gmail

| scope 예시 | 실제 범위와 집행할 행동 경계 |
| --- | --- |
| `gmail.readonly` | 메일·설정 조회. 처리 기간·라벨·본문/첨부 수집 범위는 별도로 제한 |
| `gmail.compose` | 초안 관리 **및 발신**. 초안만 맡길 때 발신 도구 비노출·정책 차단 필요 |
| `gmail.send` | 메일 발신. 수신함 읽기나 Gmail 초안 생성 권한이 아니며 `messages.send` 경로 확인 |
| `gmail.modify` | 읽기·작성·발신 및 읽음/라벨·휴지통 등 넓은 변경 범위. 허용 동작만 노출 |

위 이름의 접두사도 `https://www.googleapis.com/auth/`다. 일반 메시지를 휴지통 없이 즉시 영구 삭제하는 `messages.delete`는 더 넓은 `https://mail.google.com/`가 필요하다. 단, 초안 삭제는 compose/modify로도 가능하므로 이를 모든 삭제를 막는 권한으로 설명하지 않는다. 읽음 변경·라벨 적용·보관·휴지통·초안 삭제·일반 메시지 영구 삭제를 분리한다. [Gmail scope](https://developers.google.com/workspace/gmail/api/auth/scopes), [메시지 삭제](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages/delete), [초안 삭제](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.drafts/delete)

Gmail에 초안을 저장하는 권한은 발신에도 사용할 수 있다. 발신을 Google 권한 수준에서도 배제해야 한다면 읽기와 **로컬 초안 작성**으로 시작할 수 있다. send-only 연결에 Gmail 초안 저장·기존 초안 발송을 약속하지 않는다. [초안 생성](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.drafts/create), [초안 발신](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.drafts/send)

Gmail의 라벨·검색어·조회 기간 제한은 앱의 조회 필터와 업무 정책이며 OAuth의 계정 접근 범위를 축소하지 않는다. 공유 Calendar도 앱의 calendar ID 허용 목록과 Google의 실제 ACL을 함께 확인한다. 프롬프트에 범위를 적는 것만으로 접근 통제가 집행됐다고 판단하지 않는다.

## 3. 에이전트가 대신 할 일과 사용자에게 넘길 일

허용된 설정은 목적에 맞는 커넥터/API/CLI를 먼저 사용하고, 해당 수단에 없는 일반 설정은 사용 가능한 브라우저에서 진행한다. 기술 수단이나 역할 권한이 없을 때만 그 단계를 사용자에게 넘긴다. 이미 승인한 범위의 설정을 매 단계 다시 승인받지는 않는다.

| 단계 | 에이전트의 대리 수행 | 사용자·관리자에게 필요한 행동 |
| --- | --- | --- |
| 연결 준비 | 기능·계정·호스트 확인, 공식 문서와 실제 지원 도구 대조, 필요한 설정값 준비 | 아직 정하지 않은 목적·허용 범위 확정 |
| 구성 | 권한이 있으면 연결 설정·API 활성화·일반 콘솔 폼·callback·비밀 참조·어댑터 정책 준비 | 에이전트에게 없는 콘솔/호스트 접근 또는 조직 변경 권한 제공 여부 결정 |
| 인증 | 선택한 제품의 공식 연결 동작으로 로그인 화면 열기, 앱·scope·재개 위치 안내 | 공식 Google 화면에서 계정 선택·로그인·2단계 인증·동의 직접 수행 |
| 조직 통제 | 앱 client ID·필요 scope·대상 조직/사용자·변경 이유를 준비 | 관리자가 필요한 앱 접근만 허용; 조직 전체 신뢰·보안 해제를 기본 해법으로 사용하지 않음 |
| 검증·운영 | 운영 호스트에서 허용 표본 조회·결과 재조회·예약/재시작·오류 처리 구성 | 합의한 경우의 시험 수신자/참석자 확인, 사용자 화면에서 필요한 결과 확인 |

비밀번호·인증 코드·OAuth authorization code·access/refresh token·client secret을 대화에 붙여넣게 하지 않는다. 인증 응답 URL에도 코드가 들어갈 수 있으므로 로그·스크린샷·진행 기록에서 제거한다. 사용자에게는 공식 로그인 화면을 안내하고, 필요한 비밀은 제품의 인증 흐름이나 해당 호스트의 비밀 저장소로 직접 전달한다. [Google OAuth 보관 원칙](https://developers.google.com/identity/protocols/oauth2/resources/best-practices)

넘겨야 하는 단계에는 **정확한 화면 → 사용자가 할 행동 → 성공 신호 → 돌아온 뒤 재개할 작업**을 안내한다. 예: “선택한 연결의 Google 로그인 화면에서 지정 계정과 Calendar 읽기 범위를 확인하고 동의하세요. 연결 화면에 해당 계정이 표시되면 알려주세요. 그다음 운영 호스트에서 지정 기간의 일정 한 건을 조회하겠습니다.” 비밀값 대신 완료 여부만 받는다.

권한이 없는 관리 단계가 남아도 로컬 설정안·scope 목록·시험 계획·어댑터의 비밀 참조처럼 가능한 준비는 끝낸다. `사용자 입력 대기`와 `관리자 정책 확인 대기`를 구분하고 같은 설명을 처음부터 반복하지 않도록 재개 위치를 남긴다.

## 4. 기존 커넥터를 쓰는 실행 순서

1. 선택한 실행기의 연결 목록·버전·공식 안내에서 Calendar/Gmail 지원, 필요한 메서드와 인증 위치를 확인한다. 이 작업을 맡은 현재 에이전트의 연결과 운영 런타임의 연결을 따로 표시한다.
2. 기존 연결이 있으면 재로그인부터 하지 말고 계정·요청/허용 scope·대상 ID·만료 상태를 확인한다. 아직 연결이 없으면 제품이 제공하는 “계정 연결” 또는 공식 인증 명령으로 진행한다.
3. 대상 호스트·프로필에 설정과 자격증명 참조를 배치하고, 사용자에게 3절의 로그인·동의를 안내한다. 공용 커넥터의 내부 OAuth 앱을 사용한다면 자체 client 생성 절차는 제외한다.
4. 연결 완료 표시 뒤에도 실제 운영 프로세스에서 허용 계정·대상 표본을 조회한다. 개발 터미널에서만 되고 예약 서비스의 다른 OS 사용자에게는 안 되는 경우를 찾아 수정한다.
5. 선택한 초안·일정 변경·발신만 시험하고 결과 ID로 재조회한다. 지원하지 않는 메서드는 현재 구성의 미지원으로 기록하고 필요한 경우에만 다른 어댑터 또는 직접 OAuth를 비교한다.
6. 자동 실행을 선택했으면 트리거·토큰 갱신·실패 알림·상태 기록을 연결하고 새 대화·재시작에서도 확인한다. 연결된 API만으로 능동 실행이 시작되었다고 기록하지 않는다.

## 5. 직접 OAuth 구성이 필요한 경우

아래는 기존 연결이 부족하고 자체 어댑터를 선택했을 때만 적용한다. 계정과 업무에 맞는 공식 라이브러리를 사용하며 빠른 시작 코드를 운영 설정으로 그대로 확정하지 않는다. [Calendar 시작 안내](https://developers.google.com/workspace/calendar/api/quickstart/python)

1. **Cloud 프로젝트:** 기존 승인 프로젝트를 먼저 확인한다. 없으면 소유자·조직·운영 책임자를 정해 만들고 프로젝트 ID를 기록한다. `APIs & Services → Library`에서 선택한 Calendar API/Gmail API만 활성화한다. Drive·Sheets·Tasks도 실제 채택한 경우에만 추가한다.
2. **Branding:** `Google Auth platform → Branding`에서 미구성 상태이면 시작하고 앱 이름·지원 이메일·연락처 등 실제 소유자 정보를 입력한다. 대리할 수 있는 일반 폼은 에이전트가 준비하고 소유자 확인이 필요한 값만 요청한다.
3. **Audience:** 개인 계정·조직 밖 사용자는 External을 검토한다. Internal은 해당 Workspace/Cloud Identity 조직 내부 사용 조건이 맞을 때 선택하며 개인 Gmail에도 무조건 적용하지 않는다. Testing이면 사용할 계정을 Test users에 추가한다.
4. **Data Access:** 필요한 scope만 설정하고 실제 프로그램의 요청 scope와 대조한다. Google의 검증·조직 정책 적용 여부를 확인한다. 민감/제한 범위를 사용하는 외부 배포 앱은 추가 검증 대상이 될 수 있으며 “테스트 경고를 넘기면 운영 완료”로 처리하지 않는다. [Branding·Audience·Data Access](https://developers.google.com/workspace/guides/configure-oauth-consent)
5. **Clients:** `Google Auth platform → Clients → Create client`에서 실행 방식에 맞는 유형을 선택한다. 설치형 로컬 앱/CLI는 Desktop app, 서버 callback을 운영하는 앱은 Web application을 검토한다. 실제 화면에 `Use this client for an AI-powered agent` 선택이 있으면 용도에 맞게 판단·기록한다. [클라이언트 생성](https://developers.google.com/workspace/guides/create-credentials)

	- Desktop 흐름은 시스템 브라우저와 로컬 loopback callback, PKCE를 지원하는 공식 방식으로 구성한다. desktop client를 만들었다는 이유로 원격 서버의 인증까지 자동 해결되지는 않는다. [Desktop OAuth](https://developers.google.com/identity/protocols/oauth2/native-app)
	- Web 흐름은 운영 callback의 scheme·호스트·포트·경로를 확정해 Authorized redirect URIs와 정확히 맞춘다. 운영용 HTTPS·`state` 확인과 해당 라이브러리가 요구하는 자격 설정을 적용한다. [Web OAuth](https://developers.google.com/identity/protocols/oauth2/web-server)
	- 헤드리스 서버의 `localhost`는 로그인한 휴대폰/노트북의 `localhost`와 다르다. 선택 도구가 지원하는 원격 인증·웹 callback 또는 승인된 포트 전달 경로를 먼저 확인한다. 폐기된 OOB 코드 복사 방식이나 일반 기기 인증 흐름이 Gmail/Calendar scope를 지원한다고 가정하지 않는다.

6. **자격 보관:** 해당 client/라이브러리가 요구하는 설정을 실행 호스트의 보호된 경로·키체인·비밀 저장소에 두고 OS 서비스 사용자가 필요한 범위만 접근하게 한다. 앱 자격과 사용자 토큰을 구분하고 저장소·Obsidian·GitHub·동기화 자료에 포함하지 않는다. 문서에는 참조 위치만 기록한다.
7. **사용자 인증:** 실제 앱이 요청하는 공식 Google 로그인 흐름을 실행한다. 사용자가 계정·scope를 확인하고 동의하면 callback을 처리하고 실제 부여된 범위를 대조한다. 로그인 성공과 Gmail/Calendar 데이터 접근 성공은 별도다.
8. **지속 접근:** 사용자 부재 중 실행이 필요하면 지원되는 offline access·refresh token 갱신을 구성한다. 재동의 때 refresh token이 항상 새로 반환된다고 가정하지 말고 기존 유효 값을 빈 값으로 덮어쓰지 않는다. 갱신 실패는 제한된 재인증 흐름으로 보낸다. [갱신 절차](https://developers.google.com/identity/protocols/oauth2/web-server#offline)
9. **Testing 운영 한계:** External + Testing 앱의 refresh token은 일반적으로 **7일 만료**이며 기본 프로필 scope만 사용하는 예외가 있다. Calendar/Gmail 연결은 이 예외에 기대지 않는다. 장기 운영은 대상 배포·검증 조건을 정리하고 정책에 맞게 전환하며, 만료 때마다 자동 재동의를 반복시키는 것으로 완료 처리하지 않는다. [토큰 만료 조건](https://developers.google.com/identity/protocols/oauth2#expiration)
10. **호스트 검증:** 브라우저를 닫고 실제 운영 계정/서비스에서 허용 표본 조회와 갱신·재시작을 확인한다. 이 결과가 있어야 해당 호스트의 연결 완료로 기록한다. 인증을 끝낸 사용자의 모든 메일·캘린더를 일괄 수집하지 않는다.

## 6. 개인 계정과 Workspace의 위임을 구분한다

| 상황 | 설정과 진행 경계 |
| --- | --- |
| 개인 OAuth | 본인이 선택한 앱에 필요한 scope를 동의. 계정 비밀번호를 에이전트나 다른 사람에게 전달하는 방식으로 대체하지 않음 |
| Workspace OAuth 앱 통제 | 관리자 콘솔 `Security → Access and data control → API controls → Manage Third-Party App Access`에서 정확한 client와 서비스 접근 정책 확인. 사용자의 동의만으로 조직 차단이 해제되지 않음 |
| 공유 Calendar | 소유자 또는 공유 관리 권한자가 `Settings and sharing → Shared with`에서 대상과 필요한 권한 설정. 공유 초대 발송도 허용 범위 확인. API scope와 실제 ACL을 함께 대조 |
| Gmail 사서함 위임 | 사람이 다른 사서함을 읽고 보내고 삭제하는 위임. `Settings → See all settings → Accounts and Import/Accounts → Grant access to your account`에서 별도 설정·초대 수락. 위임 사실만으로 선택한 API 커넥터가 다른 사서함에 접근한다고 가정하지 않음 |
| 일반 서비스 계정 | 자체 데이터 또는 명시적으로 공유된 자원에 접근하는 별도 주체. Cloud IAM 역할이나 서비스 계정 생성만으로 사용자 Gmail·Calendar 접근이 생기지 않음 |
| 도메인 전체 위임(DWD) | 사용자 동의 없이 조직 사용자를 대신할 수 있는 별도 관리자 구성. 개인 시스템의 기본안에서 제외하며 일반 OAuth로 해결되면 사용하지 않음 |

[Workspace 앱 통제](https://knowledge.workspace.google.com/admin/apps/control-which-third-party-and-internal-apps-access-google-workspace-data), [Calendar 공유](https://support.google.com/calendar/answer/37082?hl=en), [Gmail 사서함 위임](https://support.google.com/mail/answer/138350?hl=en), [서비스 계정의 접근 방식](https://developers.google.com/workspace/guides/create-credentials)

DWD를 조직이 명시적으로 선택한 경우에만 **슈퍼 관리자**가 `Security → Access and data control → API controls → Manage Domain Wide Delegation`에서 client ID와 필요한 scope를 승인한다. 앱이 대신할 사용자, 허용 업무, 감사·키 관리·회수 책임도 제한한다. 도메인 전체 scope 승인만으로 특정 사용자 제한이 집행되는 것은 아니므로 앱 정책을 함께 적용한다. [공식 DWD 절차](https://developers.google.com/identity/protocols/oauth2/service-account#delegatingauthority), [DWD 최소화 권고](https://knowledge.workspace.google.com/admin/apps/domain-wide-delegation-best-practices)

## 7. 선택한 기능을 실제 결과로 검증한다

아래 표는 앞으로 수행할 검증 계획이다. 이미 합의한 표본·대상·행동 안에서 진행하며, 발신·초대·삭제를 선택하지 않았다면 **선택 제외**로 남긴다. 이를 연결 실패나 필수 미완료로 표시하지 않는다. 자신에게 보내는 시험 메일도 발신을 선택한 범위에 포함돼 있어야 한다.

| 선택 기능·경계 | 확인할 실제 증거 | 기존 검증 연결 |
| --- | --- | --- |
| 계정·권한 | 운영 호스트/프로필·연결 계정·부여 scope·대상 ID 일치, 비허용 도구/대상 차단 | V03/V09/V17 |
| Calendar 읽기 | 지정 기간의 표본 이벤트 ID·시간대·시작/종료·종일/반복 상태를 원본 화면 또는 API 결과와 대조 | V15/V21 |
| Calendar 쓰기·초대 선택 | 허용 일정 생성/변경 뒤 같은 ID로 재조회, 반복 회차·참석자·통지 상태 확인. 완료 처리와 구분 | V03/V05/V06/V21 |
| Gmail 읽기·초안 선택 | 지정 메시지/스레드·첨부 범위, 읽음/라벨 보존, 선택한 초안 ID와 내용 재조회 | V03/V05/V06 및 E01–E04 |
| Gmail 발신 선택 | 허용 발신자/수신자/내용·횟수, 제공자 결과 ID·보낸 상태·합의한 수신 확인. 접수와 전달·읽음·업무 완료를 구분 | V03/V05/V06/V09 및 E05/E06 |
| 기기·재시작·OFF | 대화 종료 후 운영 호스트 조회/예약, 중지 중 상태, 재부팅 뒤 갱신·누락 회차·중복 여부 | V07/V15/V16 |
| 비용·해제 | 쿼터/예산 한도·중단 경로, 선택한 시험 연결 회수 후 접근 차단, 재연결 범위 대조 | V03/V09/V17/V19 |

발신 전용 연결에는 재조회를 위해 읽기 scope를 임의 추가하지 않는다. 허용된 별도 조회 연결이나 사용자 화면의 확인으로 증거를 보완하고, 확인할 수 없는 부분은 미확인으로 남긴다. 이메일 세부 시험은 [E01–E08](<이메일 연결과 로컬 앱.md>), 일반 연결은 [C01–C06](<연결 대상별 설정 가이드.md>)를 재사용한다. Drive·Docs·Sheets도 연결할 때는 해당 문서의 V18 시험을 추가한다.

실제 연결 전에 [가상 시험 안내](<../40_검증/가상 시험 안내.md>)의 S18 `googleConnectionSamples`로 분기·미선택 행동·호스트 인계·대기/실패 상태를 검토할 수 있다. 이는 사람이 작성한 입력·기대 결과이며 실제 계정 인증·모델 실행·Google 서비스 검증을 대신하지 않는다.

일정·메일 쓰기는 먼저 작업 ID와 실행 의도를 저장하고 성공 응답의 외부 ID를 연결한다. 시간 초과·응답 유실이면 기존 결과부터 조회한다. 메일 발신에 일반적인 중복 방지 키가 있다고 가정하지 않으며, 보낸 결과가 불확실한 상태에서 자동 재발신하지 않는다. HTTP 성공 응답만으로 수신자 전달이나 실제 업무 완료를 확정하지 않는다. [Gmail 발신 한계](https://developers.google.com/workspace/gmail/api/guides/handle-errors)

## 8. 능동 실행·실패·연결 회수

아침 일정 정리·새 메일 요약 등을 선택하면 [능동 운영과 완료 추적](<능동 운영과 완료 추적.md>)에 따라 실제 예약/이벤트, 담당 호스트, 대상 계정, task ID·상태, 재시도·알림·비용 한도를 연결한다. 이벤트 구독 방식은 제공자가 요구하는 갱신·누락 복구를, 폴링은 커서·조회 기간·중복 제거를 구현한다. 사용자 지시 없이 실행하는 범위도 이미 정한 정책을 따른다.

Google 클라우드에 일정·메일이 저장되는 것과 담당 에이전트가 실행되는 것은 별개다. 집 PC가 꺼져도 Gmail 수신·Calendar 화면은 이용할 수 있지만 그 PC의 조회·요약·예약 실행은 중단된다. 별도 상시 런타임을 선택했다면 그 호스트의 자격과 실행 증거를 따로 확인한다. 새 호스트로 옮길 때는 기존 담당을 멈추고 상태·권한·미완료 결과를 대조해 중복 작업자를 만들지 않는다.

| 증상 | 확인·복구 순서 |
| --- | --- |
| 401·만료 access token | 지원 라이브러리로 갱신 → 실제 scope 확인 → 갱신 실패 시 공식 재인증 안내. 무한 로그인 반복 금지 |
| `invalid_grant`·7일 뒤 중단 | 회수·Testing 만료·계정/관리자 정책과 토큰 저장 여부 확인 → 해당 원인 해결 뒤 재인증 |
| 403 | 오류 reason으로 scope 부족·대상 ACL·API 비활성·조직 차단·할당량을 구분. 무조건 전체 scope나 DWD로 확대하지 않음 |
| `redirect_uri_mismatch`·callback 미도착 | client 유형·등록 URI와 실제 주소·로컬/원격 호스트·포트·HTTPS 확인. 인증 코드를 채팅으로 복사해 해결하지 않음 |
| 429·일부 403 quota 오류 | 제공된 재시도 시간·지수 백오프·분산 지연·횟수/예산 상한 적용. 다른 계정으로 한도를 우회하지 않음 |
| 시간 초과·5xx | 재조회로 이미 처리됐는지 확인 → 읽기는 제한된 재시도, 쓰기는 결과 불명·중복 위험을 기록하고 복구 |
| 수동 조회는 되나 자동 실행 중단 | 호스트 전원·서비스 사용자·토큰 접근·트리거·네트워크·시간대 확인. Google 인증 오류와 구분 |

오류는 상태 코드뿐 아니라 원인 필드로 판단한다. [Calendar 오류](https://developers.google.com/workspace/calendar/api/guides/errors), [Gmail 오류](https://developers.google.com/workspace/gmail/api/guides/handle-errors)

무료 사용 범위와 한도는 **현재 프로젝트의 공식 quota·과금 정책**으로 확인한다. Calendar/Gmail API를 영구 무제한 무료로 단정하지 않으며 모델·호스트·저장소 비용도 분리한다. 과금 계정 연결·유료 자원·한도 증액은 기본 설정에 포함하지 않고 선택한 비용 정책에 따라 결정한다. [Calendar 한도](https://developers.google.com/workspace/calendar/api/guides/quota), [Gmail 한도](https://developers.google.com/workspace/gmail/api/reference/quota)

연결 해제는 해당 트리거/작업자를 중지하고 제품의 연결 해제·토큰 회수를 수행한 뒤 운영 호스트에서 접근이 막히는지 확인한다. 사용자는 Google 계정의 연결된 앱에서 해당 데이터 접근을 제거할 수 있다. Workspace 앱 통제·공유 Calendar·사서함 위임·DWD를 별도로 설정했다면 그 경로도 각각 회수한다. 이미 수집한 원문·요약·검색 사본은 정한 보존/삭제 정책으로 처리하며, OAuth 해제가 기존 사본 삭제까지 대신한다고 가정하지 않는다. [Google 연결 관리](https://support.google.com/accounts/answer/13533235), [토큰 회수·보관](https://developers.google.com/identity/protocols/oauth2/resources/best-practices)

## 9. 기존 기록으로 인계한다

- [구축 결정·규칙 기록](<../30_양식/구축 결정·규칙 기록.md>): 계정/대상·업무별 허용 행동·scope·운영 호스트·대안·비용·회수 정책을 기록한다. 비밀값은 넣지 않는다.
- [셋업 진행 기록](<../30_양식/셋업 진행 기록.md>): 에이전트가 끝낸 설정, 사용자/관리자에게 남은 화면과 행동, 성공 신호·재개 작업을 기록한다.
- [검증·운영 기록](<../30_양식/검증·운영 기록.md>): 실제 표본·외부 결과 ID·호스트·기대/실제 결과·오류·복구 증거와 선택 제외 사유를 기록한다. 새 빈 양식이나 최상위 검증 번호는 만들지 않는다.

최종 보고에서는 `설정안 준비`, `사용자 인증 대기`, `해당 호스트 연결 확인`, `선택 기능 검증`, `능동 운영 검증`을 구분한다. Google 로그인 화면을 통과했거나 이 문서를 작성했다는 이유만으로 전체 연결·자동 운영을 완료로 표시하지 않는다.
