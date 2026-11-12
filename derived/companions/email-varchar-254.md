---
slug: "email-varchar-254"
why: "email-limits"
---

# Email addresses: varchar(254)

## Full rule

Use `varchar(254)` for an email address. Use 320 only with a very good reason.

Because: 320 is the RFC maximum, but 254 is the practical limit that mail servers along the way enforce.

## Why this rule exists

### Story: Two limits on one address

The two numbers in the email rule look oddly specific, and each comes from a different place.

The first is 320. Under the standard (RFC 5321), the part before the `@` can be up to 64 characters and the domain after it up to 255, so 64 plus the `@` plus 255 is 320. On the rules for how an address looks, an address that long is valid.

The second is 254, and it comes from a separate rule about the SMTP conversation between mail servers. The address travels inside a path that is limited to 256 characters, and the path includes the angle brackets around the address. That leaves 254 for the address itself.

The two limits are like the rules for addressing a letter. The post office might accept an address of one length, while the standard envelope fits only a shorter one. An address can be valid by the post office's own rules and still not fit the envelope that so many hops along the way happen to use. An address of 320 characters is valid on paper, but many servers between sender and recipient enforce the shorter limit, and the message can bounce off infrastructure nobody controls.

So the practical limit is 254, which is why the standard uses `varchar(254)`. A column wider than that would only invite addresses that cannot be delivered anyway.
