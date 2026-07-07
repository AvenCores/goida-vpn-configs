package main

type AhoCorasick struct {
	root *acNode
}

type acNode struct {
	children [128]*acNode
	fail     *acNode
	isEnd    bool
}

// NewAhoCorasick builds a DFA trie from a list of lowercase patterns
func NewAhoCorasick(patterns []string) *AhoCorasick {
	root := &acNode{}
	for _, pattern := range patterns {
		// Skip patterns containing non-ASCII bytes entirely —
		// stripping only non-ASCII bytes would leave broken fragments
		// (e.g. "честныйзнак.рф" → "." which matches everything)
		hasNonASCII := false
		for i := 0; i < len(pattern); i++ {
			if pattern[i] >= 128 {
				hasNonASCII = true
				break
			}
		}
		if hasNonASCII || len(pattern) == 0 {
			continue
		}

		curr := root
		for i := 0; i < len(pattern); i++ {
			b := pattern[i]
			if curr.children[b] == nil {
				curr.children[b] = &acNode{}
			}
			curr = curr.children[b]
		}
		curr.isEnd = true
	}

	// BFS to build failure links and transition table DFA
	var queue []*acNode
	for i := 0; i < 128; i++ {
		if root.children[i] != nil {
			root.children[i].fail = root
			queue = append(queue, root.children[i])
		} else {
			root.children[i] = root
		}
	}

	for len(queue) > 0 {
		curr := queue[0]
		queue = queue[1:]

		for i := 0; i < 128; i++ {
			child := curr.children[i]
			if child != nil {
				child.fail = curr.fail.children[i]
				if child.fail.isEnd {
					child.isEnd = true
				}
				queue = append(queue, child)
			} else {
				curr.children[i] = curr.fail.children[i]
			}
		}
	}

	return &AhoCorasick{root: root}
}

// MatchLower runs the DFA over the text, lowercasing ASCII characters on the fly.
// This achieves case-insensitive matching with 0 memory allocation!
func (ac *AhoCorasick) MatchLower(text string) bool {
	curr := ac.root
	for i := 0; i < len(text); i++ {
		b := text[i]
		if b >= 'A' && b <= 'Z' {
			b = b + 32 // lowercase on-the-fly
		}
		if b >= 128 {
			curr = ac.root
			continue
		}
		curr = curr.children[b]
		if curr.isEnd {
			return true
		}
	}
	return false
}
