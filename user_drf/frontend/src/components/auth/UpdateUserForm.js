import React from "react";
import { Field, reduxForm, SubmissionError } from "redux-form";
import { connect } from "react-redux";
import injectSheet from "react-jss";

import history from "../../history";
import { renderDatePicker } from "../DateTimePicker";
import { updateUser, fetchUser } from "../../actions/auth";
import ButtonLoader from "../ButtonLoader";
import ChangePasswordForm from "./ChangePasswordForm";

const styles = {
  list: {
    width: "45%"
  },
  "@media screen and (max-width: 900px)": {
    list: {
      width: "70%"
    }
  },
  "@media screen and (max-width: 730px)": {
    list: {
      width: "85%"
    }
  }
};

class UpdateUserForm extends React.Component {
  componentWillMount() {
    if (!this.props.user.isSignedIn) {
      this.props.fetchUser();
    }
    this.props.initialize(this.props.user);
  }

  componentDidUpdate() {
    if (!this.props.user.isSignedIn) {
      history.push("/");
    }
    if (this.props.pristine) {
      this.props.initialize(this.props.user);
    }
  }

  renderError({ error }) {
    if (error) {
      return (
        <div className="ui error message">
          <div className="header">{error}</div>
        </div>
      );
    }
  }

  renderInput = ({ input, label, meta }) => {
    const className = `field ${meta.error && meta.touched ? "error" : ""}`;
    return (
      <div className={className}>
        <label>{label}</label>
        <input {...input} />
        {this.renderError(meta)}
      </div>
    );
  };

  // function is async so we could make use of server
  // side validation and return errors from server
  // which is only avaliable when onSubmit returns a promise
  onUpdateUser = async formValues => {
    // if it's a new date, get it to appropriate format
    if (formValues.date_of_birth instanceof Date) {
      const { date_of_birth: dob } = formValues;
      const date = `${dob.getFullYear()}-${dob.getMonth() +
        1}-${dob.getDate()}`;

      await this.props.updateUser({ ...formValues, date_of_birth: date });
    } else {
      await this.props.updateUser(formValues);
    }
    const errors = this.props.errors.update;
    if (errors) {
      throw new SubmissionError({ ...errors });
    }
  };

  hasErrors = () => {
    return !this.props.valid;
  };

  render() {
    const { classes } = this.props;

    return (
      <div className={classes.list}>
        <form
          onSubmit={this.props.handleSubmit(this.onUpdateUser)}
          className="ui form error"
        >
          <Field
            name="first_name"
            component={this.renderInput}
            label="First Name"
          />
          <Field
            name="last_name"
            component={this.renderInput}
            label="Last Name"
          />
          <Field
            name="date_of_birth"
            component={renderDatePicker}
            label="Date of birth"
          />
          <ButtonLoader
            style={{ marginTop: 15 }}
            buttonText="Update Information"
            onSubmit={this.props.handleSubmit(this.onUpdateUser)}
            hasErrors={this.hasErrors}
            delay={1000}
          />
        </form>
        <div style={{ marginTop: 20 }}>
          <p>Change Password:</p>
          <ChangePasswordForm />
        </div>
      </div>
    );
  }
}

const validate = formValues => {
  const errors = {};
  const { first_name, last_name, date_of_birth } = formValues;
  if (first_name && first_name.length >= 30) {
    errors.first_name = "Your first name is too long";
  }
  if (last_name && last_name.length >= 30) {
    errors.last_name = "Your last name is too long";
  }

  if (date_of_birth && date_of_birth.length > 10) {
    errors.date_of_birth = "Use date picker to select date";
  }
  return errors;
};

const mapStateToProps = ({ user }) => {
  return {
    user,
    errors: user.errors
  };
};

const styled = injectSheet(styles)(UpdateUserForm);

const formWrapperd = reduxForm({
  form: "updateUserForm",
  validate
})(styled);

export default connect(
  mapStateToProps,
  { updateUser, fetchUser }
)(formWrapperd);
