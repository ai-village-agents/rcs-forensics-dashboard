(function () {
  function byId(id) {
    return document.getElementById(id);
  }

  function renderTimeline(data) {
    var root = byId('milestone-timeline-root');
    var status = byId('milestone-timeline-status');
    if (!root) return;

    if (!data || !Array.isArray(data.milestones) || data.milestones.length === 0) {
      if (status) {
        status.textContent = 'No milestones have been registered in the canonical JSON yet.';
      }
      return;
    }

    root.innerHTML = '';

    data.milestones.sort(function (a, b) {
      if (a.sort_key && b.sort_key) {
        return String(a.sort_key).localeCompare(String(b.sort_key));
      }
      if (a.date && b.date) {
        return String(a.date).localeCompare(String(b.date));
      }
      return 0;
    });

    data.milestones.forEach(function (m) {
      var item = document.createElement('article');
      item.className = 'timeline-item';

      var title = document.createElement('div');
      title.className = 'timeline-title';
      title.textContent = m.label || m.id || 'RCS milestone';
      item.appendChild(title);

      var meta = document.createElement('div');
      meta.className = 'timeline-meta';
      var parts = [];
      if (m.date) parts.push(m.date);
      if (m.rcs_span) parts.push('RCS span: ' + m.rcs_span);
      if (m.rcs_commit) parts.push('RCS head ' + m.rcs_commit);
      meta.textContent = parts.join(' · ');
      item.appendChild(meta);

      if (Array.isArray(m.tags) && m.tags.length) {
        var tagsContainer = document.createElement('div');
        m.tags.forEach(function (tag) {
          var pill = document.createElement('span');
          pill.className = 'timeline-tag';
          pill.textContent = tag;
          tagsContainer.appendChild(pill);
        });
        item.appendChild(tagsContainer);
      }

      if (m.description) {
        var desc = document.createElement('p');
        desc.textContent = m.description;
        item.appendChild(desc);
      }

      if (m.report) {
        var link = document.createElement('a');
        link.className = 'timeline-link';
        link.href = m.report;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.textContent = 'Open report (' + m.report + ')';
        item.appendChild(link);
      }

      root.appendChild(item);
    });

    if (status) {
      var count = data.milestones.length;
      status.textContent =
        'Loaded ' + count + ' milestone' + (count === 1 ? '' : 's') +
        ' from canonical JSON in this repository (rendered as a live-only view).';
    }
  }

  function renderTagSummary(milestones) {
    var root = byId('milestone-tag-summary-root');
    var status = byId('milestone-tag-summary-status');
    if (!root || !status) return;

    if (!Array.isArray(milestones) || milestones.length === 0) {
      status.textContent = 'No milestones available for tag summary yet.';
      return;
    }

    var counts = {};
    milestones.forEach(function (m) {
      if (Array.isArray(m.tags)) {
        m.tags.forEach(function (tag) {
          var key = String(tag);
          counts[key] = (counts[key] || 0) + 1;
        });
      }
    });

    root.innerHTML = '';

    Object.keys(counts).sort().forEach(function (tag) {
      var row = document.createElement('div');
      row.className = 'tag-summary-row';

      var tagLabel = document.createElement('span');
      tagLabel.className = 'tag-summary-tag';
      tagLabel.textContent = tag;

      var countLabel = document.createElement('span');
      countLabel.className = 'tag-summary-count';
      var count = counts[tag];
      countLabel.textContent = count + ' report' + (count === 1 ? '' : 's');

      row.appendChild(tagLabel);
      row.appendChild(countLabel);
      root.appendChild(row);
    });

    status.textContent = 'Tag summary computed live in your browser from canonical milestone JSON.';
  }

  function init() {
    var root = byId('milestone-timeline-root');
    var status = byId('milestone-timeline-status');
    if (!root || !status) return;

    status.textContent = 'Loading milestone JSON…';

    fetch('data/rcs_milestones.json', { cache: 'no-cache' })
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(function (data) {
        renderTimeline(data);
        renderTagSummary(data.milestones);
      })
      .catch(function () {
        if (status) {
          status.textContent =
            'Could not load milestone JSON (treated as a live-only failure). You can still open the written reports directly from this repository.';
        }
        var tagStatus = byId('milestone-tag-summary-status');
        if (tagStatus) {
          tagStatus.textContent =
            'Could not compute the tag summary because the milestone JSON failed to load (live-only failure).';
        }
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
