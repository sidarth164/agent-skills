# GitBook Custom Blocks Reference

GitBook extends standard GitHub Flavored Markdown with custom block syntax. This reference
covers every block type with full syntax examples.

## Table of Contents

- [Tabs](#tabs)
- [Stepper](#stepper)
- [Hints](#hints)
- [Expandable](#expandable)
- [Columns](#columns)
- [Updates](#updates)
- [Cards](#cards)
- [Embeds](#embeds)
- [Files](#files)
- [Buttons](#buttons)
- [Icons](#icons)
- [Reusable Content](#reusable-content)
- [Code Blocks with Titles](#code-blocks-with-titles)
- [OpenAPI](#openapi)
- [Variables and Expressions](#variables-and-expressions)
- [Page Frontmatter](#page-frontmatter)

---

## Tabs

Present alternative content — different languages, platform-specific instructions, config options.

````markdown
{% tabs %}
{% tab title="JavaScript" %}
```javascript
const greeting = 'Hello World';
console.log(greeting);
```
{% endtab %}

{% tab title="Python" %}
```python
greeting = "Hello World"
print(greeting)
```
{% endtab %}
{% endtabs %}
````

---

## Stepper

Sequential, multi-step processes where order matters.

```markdown
{% stepper %}
{% step %}
## First step

Complete the initial setup by installing dependencies.
{% endstep %}

{% step %}
## Second step

Configure your environment variables in `.env`.
{% endstep %}

{% step %}
## Third step

Run the application with `npm start`.
{% endstep %}
{% endstepper %}
```

---

## Hints

Highlight important information. Styles: `info`, `warning`, `danger`, `success`.

```markdown
{% hint style="info" %}
This is an informational hint with helpful context.
{% endhint %}

{% hint style="warning" %}
Be careful when running this command in production.
{% endhint %}

{% hint style="danger" %}
This action cannot be undone. Make sure you have backups.
{% endhint %}

{% hint style="success" %}
Your configuration has been saved successfully!
{% endhint %}
```

---

## Expandable

Optional content that doesn't need to be visible by default. Uses standard HTML `<details>`.

````markdown
<details>
<summary>Advanced Configuration Options</summary>

Detailed information about advanced settings.

```yaml
advanced:
  option1: value1
  option2: value2
```
</details>
````

---

## Columns

Side-by-side content (2 columns maximum).

```markdown
{% columns %}
{% column %}
### Before

Old implementation that was inefficient.
{% endcolumn %}

{% column %}
### After

New optimized approach with better performance.
{% endcolumn %}
{% endcolumns %}
```

---

## Updates

Product updates, release notes, changelogs. Entries in reverse chronological order.

```markdown
{% updates format="full" %}
{% update date="2024-01-15" %}
# Version 2.0 Released

New features including dark mode and improved search.
{% endupdate %}

{% update date="2024-01-01" %}
# Bug Fixes

Fixed several issues reported by the community.
{% endupdate %}
{% endupdates %}
```

---

## Cards

Clickable navigation elements. Uses HTML tables with special attributes.

```markdown
<table data-view="cards">
    <thead>
        <tr>
            <th>Title</th>
            <th data-card-target data-type="content-ref">Target</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Getting Started Guide</td>
            <td><a href="getting-started/quickstart.md">Quick Start</a></td>
        </tr>
        <tr>
            <td>API Reference</td>
            <td><a href="api-reference/overview.md">API Docs</a></td>
        </tr>
    </tbody>
</table>
```

---

## Embeds

Include external content — videos, interactive demos, social media.

```markdown
{% embed url="https://www.youtube.com/watch?v=dQw4w9WgXcQ" %}

{% embed url="https://codepen.io/username/pen/example" %}
```

---

## Files

Downloadable files with captions.

```markdown
{% file src="https://example.com/document.pdf" %}
Complete documentation in PDF format.
{% endfile %}
```

---

## Buttons

Call-to-action links. Styles: `primary`, `secondary`.

```markdown
<a href="https://example.com/download" class="button primary">Download Now</a>

<a href="https://docs.example.com" class="button secondary">View Documentation</a>
```

With icons (Font Awesome names without `fa-` prefix):

```markdown
<a href="https://github.com/user/repo" class="button primary" data-icon="github">View on GitHub</a>
```

---

## Icons

Inline icons from Font Awesome for visual indicators.

```markdown
<i class="fa-check">check</i> Feature enabled
<i class="fa-warning">warning</i> Requires configuration
<i class="fa-info-circle">info</i> Learn more
```

---

## Reusable Content

Sync content across multiple pages. Blocks are created through GitBook UI and given unique IDs.

```markdown
{% include "/reusable-content/rc12345" %}
```

---

## Code Blocks with Titles

````markdown
{% code title="index.js" %}
```javascript
const foo = 'bar';
console.log(foo);
```
{% endcode %}
````

---

## OpenAPI

OpenAPI specs cannot be embedded directly in markdown. They must be uploaded via the GitBook
API, CLI, or UI first. Once uploaded, reference them:

```markdown
{% openapi src="https://api.example.com/openapi.json" path="/users" method="get" %}
[https://api.example.com/openapi.json](https://api.example.com/openapi.json)
{% endopenapi %}
```

---

## Variables and Expressions

### Defining Variables

**Space-level** in `docs/.gitbook/vars.yaml`:
```yaml
project_name: Acme
latest_version: v3.0.4
```

**Page-level** in frontmatter:
```yaml
---
vars:
  page_version: v2.1.0
---
```

### Using Variables

Expressions use JavaScript syntax in a special code tag:

```markdown
<!-- Space variable -->
<code class="expression">space.vars.latest_version</code>

<!-- Page variable -->
<code class="expression">page.vars.page_version</code>

<!-- String concatenation -->
<code class="expression">"Version: " + space.vars.latest_version</code>

<!-- Conditional -->
<code class="expression">space.vars.latest_version === "v3.0.4" ? "Latest" : "Outdated"</code>
```

---

## Page Frontmatter

All available fields:

```yaml
---
description: Page description for SEO and llms.txt
icon: book-open                    # Font Awesome icon name
hidden: true                       # Hide from table of contents
vars:
  my_variable: value
if: visitor.claims.unsigned.condition   # Adaptive content visibility
layout:
  width: default                   # or 'wide'
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---
```

- `description` — always set this; it feeds into llms.txt and search
- `icon` — Font Awesome names: `book-open`, `bolt`, `stars`, `brackets-curly`
- `layout.width: wide` — useful for pages with wide tables or code blocks

---

## Nested Markdown

Standard markdown works inside all custom blocks:

````markdown
{% tabs %}
{% tab title="Example" %}
This tab contains markdown:

- Bullet points work
  - Nested bullets too
- **Bold text** and *italic text*

```javascript
const example = true;
```
{% endtab %}
{% endtabs %}
````

---

## Common Mistakes

- **Unclosed blocks**: Always match `{% tab %}` with `{% endtab %}`, etc.
- **Wrong nesting**: Tabs can contain hints and steppers, but verify rendering
- **Missing blank lines**: Leave blank lines before and after custom block tags
- **Tab indentation in SUMMARY.md**: Use spaces, never tabs
