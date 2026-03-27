"""Layer 1: Structural validation.

Validates that every skill in the repository has a well-formed SKILL.md
with the required frontmatter fields. No API calls — safe to run on every
commit without credentials.
"""

import pytest
from skills_ref import validate


@pytest.mark.structure
def test_skill_structure(skill_path):
    """Skill directory must pass skills-ref structural validation."""
    validate(skill_path)
