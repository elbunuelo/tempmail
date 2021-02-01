import React from "react";
import sanitizeHtml from "sanitize-html";
import dayjs from "dayjs";

import "./App.scss";

interface Mailbox {
  mailbox: string;
  token: string;
}

interface Emails {
  mailbox: string;
  emails: Email[];
}

class Email {
  body = "";
  headers: any;
  recipients: string[] = [];
  sender = "";
}

const requestMailbox = async (): Promise<Mailbox> => {
  const data = await fetch(`/api/mailbox`, {
    method: "POST",
    mode: "cors",
  });

  return data.json();
};

const getEmails = async (token: string): Promise<Emails> => {
  const data = await fetch(`/api/${token}`, {
    mode: "cors",
  });
  return data.json();
};

const Message = (props: any): React.ReactElement => {
  const email: Email = props.email;
  const [active, setActive] = React.useState(false);

  const { From: sender, Subject: subject, Date: date } = email.headers;
  const content = email.body
    .split("\r\n\r\n")
    .slice(1)
    .join("<br/>");

  return (
    <div className="email">
      <div
        className={`header ${active && "active"}`}
        onClick={() => setActive(!active)}
      >
        <span className="sender">
          {sender.substring(0, sender.indexOf("<")).trim()}
        </span>
        <span className="subject">{subject}</span>
        <span className="date">{dayjs(date).format("hh:mm")}</span>
      </div>
      {active && (
        <div
          className="body"
          dangerouslySetInnerHTML={{
            __html: sanitizeHtml(content),
          }}
        />
      )}
    </div>
  );
};

const App = (): React.ReactElement => {
  const [mailbox, setMailbox] = React.useState<string>("");
  const [emails, setEmails] = React.useState<Email[]>([]);
  const [token, setToken] = React.useState<string>("");

  React.useEffect(() => {
    if (!token) {
      return;
    }

    const requestEmails = () => {
      getEmails(token).then((data: Emails) => {
        setEmails(data.emails);
      });
    };
    const interval = setInterval(requestEmails, 10000);
    requestEmails();

    return () => clearInterval(interval);
  }, [token]);

  React.useEffect(() => {
    requestMailbox().then((data: Mailbox) => {
      setMailbox(data.mailbox);
      setToken(data.token);
    });
  }, []);

  return (
    <div className="App">
      <div className="mailbox">{mailbox}</div>
      <div className="emails">
        {emails.map((email, index) => (
          <Message key={index} email={email} />
        ))}
      </div>
    </div>
  );
};

export default App;
