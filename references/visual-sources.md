# Sources for illustrations and stock photos

Recommended sources accepted by the lecturer on 2026-09-17. License pages reviewed on that date. This is a sourcing shortlist, not approval of every individual asset.

| Source | Use in this course | License and attribution |
| --- | --- | --- |
| [unDraw](https://undraw.co/illustrations) | Consistent vector illustrations for conceptual scenes; use a restrained palette compatible with FIPU blue. | [License](https://undraw.co/license): free use and modification, including commercial projects; attribution not required. Restrictions include competing asset services, asset-pack redistribution, and AI/ML training. Check the current terms before automated retrieval. |
| [Unsplash](https://unsplash.com) | Real-world photographs of hardware, data centres, infrastructure, and people working with systems. | [Free-collection license](https://unsplash.com/license): free use and modification; attribution appreciated but not required. Unsplash+ has separate terms. Do not sell unmodified images or reproduce a competing collection. |
| [Pexels](https://www.pexels.com) | Stock photographs and short video clips where motion helps explain a concrete example. | [License](https://www.pexels.com/license/): free use and modification without mandatory attribution, including presentations and YouTube. Observe restrictions on implied endorsement, portrayal of identifiable people, and resale/redistribution. |
| [Wikimedia Commons](https://commons.wikimedia.org) | Specific equipment, historical computing images, and existing technical illustrations. | [Reuse guidance](https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia): inspect the individual file page; attribution and share-alike requirements depend on the asset. Preserve author, license, and modification information. |

## Selection and provenance

- Prefer original editable diagrams for protocols, message ordering, system boundaries, failures, and course processes. Stock illustrations should serve an explanatory purpose.
- Use SVG for vector illustrations in HTML. Provide an appropriate PDF or PNG derivative when needed for printed output, following COURSE.md.
- Before using an asset, inspect the full image and its individual source/license page. Record asset title, creator, exact URL, license/version, access date, modifications, and required credit in the lecture's `sources.md`.
- Keep downloaded originals and editable derivatives in the lecture's `assets/` directory. Put only genuinely reusable assets in `assets/shared/`.
- Required attribution must survive student-facing HTML/PDF exports and recorded presentations. Internal provenance notes alone do not fulfil a public attribution requirement.
- Document proposed visuals and their teaching purpose in the lecture's `illustrations.md`. Verify selected assets in the rendered outputs; a source recommendation is not a completed asset review.

Lecture 00's specific proposals are in [its illustration plan](../lectures/00-course-introduction/illustrations.md).

## Download command

Use `just download-image 'DIRECT_HTTPS_IMAGE_URL' 'lectures/00-course-introduction/assets/filename.svg'`.

The command accepts PNG, JPEG, GIF, WebP, and SVG images up to 25 MiB. It checks the actual image format, allows HTTPS redirects only, writes only beneath project asset directories, and refuses to overwrite existing files. URLs must point to the image itself. Record source-page and license information separately in the lecture's `sources.md`.

The scoped approval prefix is `just download-image`; this does not approve arbitrary shell commands. Network permission remains controlled by the execution environment.
